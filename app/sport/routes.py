from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from model.sport import Sport
from database.database import db
from . import bp




@bp.route('/create_sport', methods=['POST'])
def create_sport():
    try:
        data = request.get_json()
        sport_name = data.get('sport_name')

        # Check if a sport with the same name already exists (case-insensitive)
        existing_sport = Sport.query.filter(Sport.sport_name.ilike(sport_name)).first()
        if existing_sport:
            return jsonify({'success': False, 'message': 'Sport already exists'}), 400

        # Create a new sport
        sport = Sport(sport_name=sport_name)
        db.session.add(sport)
        db.session.commit()

        return jsonify({'success': True, 'sport': {'id': sport.id, 'sport_name': sport.sport_name}}), 201
    except IntegrityError as e:
        db.session.rollback()  # Rollback the transaction in case of error
        return jsonify({'success': False, 'message': 'Error creating sport: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get sports by name
@bp.route('/get_sports/<string:sport_name>', methods=['GET'])
def get_sports_by_name(sport_name):
    try:
        # Find sports by name (case-insensitive)
        sports = Sport.query.filter(Sport.sport_name.ilike(f'%{sport_name}%')).all()

        if not sports:
            return jsonify({'success': False, 'message': 'No sports found with the provided name'}), 404

        return jsonify({'success': True, 'sports': [{'id': sport.id, 'sport_name': sport.sport_name} for sport in sports]}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get all sports
@bp.route('/get_all_sports', methods=['GET'])
def get_all_sports():
    try:
        sports = Sport.query.all()

        if not sports:
            return jsonify({'success': False, 'message': 'No sports found'}), 404

        return jsonify({'success': True, 'sports': [{'id': sport.id, 'sport_name': sport.sport_name} for sport in sports]}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get a sport by ID
@bp.route('/get_sport/<int:id>', methods=['GET'])
def get_sport_by_id(id):
    try:
        sport = Sport.query.get(id)

        if not sport:
            return jsonify({'success': False, 'message': 'Sport not found'}), 404

        return jsonify({'success': True, 'sport': {'id': sport.id, 'sport_name': sport.sport_name}}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to update a sport by ID
@bp.route('/update_sport/<int:id>', methods=['PUT'])
def update_sport_by_id(id):
    try:
        data = request.get_json()
        sport_name = data.get('sport_name')

        sport = Sport.query.get(id)
        if not sport:
            return jsonify({'success': False, 'message': 'Sport not found'}), 404

        sport.sport_name = sport_name
        db.session.commit()

        return jsonify({'success': True, 'sport': {'id': sport.id, 'sport_name': sport.sport_name}}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to delete a sport by ID
@bp.route('/delete_sport/<int:id>', methods=['DELETE'])
def delete_sport_by_id(id):
    try:
        sport = Sport.query.get(id)

        if not sport:
            return jsonify({'success': False, 'message': 'Sport not found'}), 404

        db.session.delete(sport)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Sport deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
