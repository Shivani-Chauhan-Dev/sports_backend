from flask import Flask, request, jsonify
from model.review import Review
from model.athlete import Athlete
from model.coach import Coach
from database.database import db
from . import bp
from sqlalchemy.orm.exc import NoResultFound



@bp.route('/create_review', methods=['POST'])
def create_review():
    try:
        data = request.get_json()
        athlete_id = data.get('athlete_id')
        coach_id = data.get('coach_id')

        # Check if athlete_id exists
        athlete = Athlete.query.get(athlete_id)
        if not athlete:
            return jsonify({'success': False, 'message': 'Athlete not found'}), 404

        # Check if coach_id exists
        coach = Coach.query.get(coach_id)
        if not coach:
            return jsonify({'success': False, 'message': 'Coach not found'}), 404

        # Create a new review
        review = Review(
            athlete_id=athlete_id,
            coach_id=coach_id,
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        db.session.add(review)
        db.session.commit()

        return jsonify({'success': True, 'review': {'id': review.id, 'athlete_id': review.athlete_id, 'coach_id': review.coach_id, 'rating': review.rating, 'comment': review.comment}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get all reviews
@bp.route('/get_all_reviews', methods=['GET'])
def get_all_reviews():
    try:
        reviews = Review.query.all()

        if not reviews:
            return jsonify({'success': False, 'message': 'No reviews found'}), 404

        return jsonify({'success': True, 'reviews': [{'id': review.id, 'athlete_id': review.athlete_id, 'coach_id': review.coach_id, 'rating': review.rating, 'comment': review.comment} for review in reviews]}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get review by ID
@bp.route('/get_review/<int:id>', methods=['GET'])
def get_review_by_id(id):
    try:
        review = Review.query.get(id)

        if not review:
            return jsonify({'success': False, 'message': 'Review not found'}), 404

        return jsonify({'success': True, 'review': {'id': review.id, 'athlete_id': review.athlete_id, 'coach_id': review.coach_id, 'rating': review.rating, 'comment': review.comment}}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to update review by ID
@bp.route('/update_review/<int:id>', methods=['PUT'])
def update_review_by_id(id):
    try:
        data = request.get_json()
        review = Review.query.get(id)

        if not review:
            return jsonify({'success': False, 'message': 'Review not found'}), 404

        review.rating = data.get('rating', review.rating)
        review.comment = data.get('comment', review.comment)
        db.session.commit()

        return jsonify({'success': True, 'review': {'id': review.id, 'athlete_id': review.athlete_id, 'coach_id': review.coach_id, 'rating': review.rating, 'comment': review.comment}}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to delete review by ID
@bp.route('/delete_review/<int:id>', methods=['DELETE'])
def delete_review_by_id(id):
    try:
        review = Review.query.get(id)

        if not review:
            return jsonify({'success': False, 'message': 'Review not found'}), 404

        db.session.delete(review)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Review deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500