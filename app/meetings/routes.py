from flask import Flask, request, jsonify
from model.meeting import Meeting
from datetime import datetime
from model.athlete import Athlete
from model.coach import Coach
from database.database import db
from . import bp
from sqlalchemy import func, extract,or_,and_
from sqlalchemy.orm.exc import NoResultFound






@bp.route('/meetings', methods=['POST'])
def schedule_meeting():
    data = request.json
    meeting = Meeting(
        coach_id=data['coach_id'],
        athlete_id=data['athlete_id'],
        title=data['title'],
        description=data.get('description', ''),
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        status='pending'  # Coach decides later
    )
    db.session.add(meeting)
    db.session.commit()
    return jsonify(meeting.to_dict()), 201


@bp.route('/meetings/<int:meeting_id>/status', methods=['PATCH'])
def update_status(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    new_status = request.json.get('status')

    if new_status not in ['accepted', 'declined']:
        return jsonify({'error': 'Status must be accepted or declined'}), 400

    # If accepting, check for time conflict
    if new_status == 'accepted':
        conflict = Meeting.query.filter(
            Meeting.coach_id == meeting.coach_id,
            Meeting.status == 'accepted',
            Meeting.id != meeting.id,
            or_(
                and_(Meeting.start_time <= meeting.start_time, Meeting.end_time > meeting.start_time),
                and_(Meeting.start_time < meeting.end_time, Meeting.end_time >= meeting.end_time),
                and_(Meeting.start_time >= meeting.start_time, Meeting.end_time <= meeting.end_time)
            )
        ).first()

        if conflict:

            db.session.delete(meeting)
            db.session.commit()
            return jsonify({'error': 'Coach is busy. Meeting automatically declined and removed.'}), 409

    if new_status == 'declined':
        db.session.delete(meeting)
        db.session.commit()
        return jsonify({'message': 'Meeting declined and deleted.'}), 200

    meeting.status = new_status
    db.session.commit()
    return jsonify(meeting.to_dict()), 200
    #         meeting.status = 'declined'
    #         db.session.commit()
    #         return jsonify({'error': 'Coach is busy. Meeting automatically declined.'}), 409

    # meeting.status = new_status
    # db.session.commit()
    # return jsonify(meeting.to_dict())

@bp.route('/coaches/<int:coach_id>/meetings', methods=['GET'])
def get_coach_meetings(coach_id):
    meetings = Meeting.query.filter_by(coach_id=coach_id).order_by(Meeting.start_time).all()

    return jsonify([meeting.to_dict() for meeting in meetings]), 200
