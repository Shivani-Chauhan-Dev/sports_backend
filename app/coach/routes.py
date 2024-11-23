from flask import Flask, request, jsonify
from model.coach import Coach
from database.database import db
from . import bp
from sqlalchemy.orm.exc import NoResultFound



# Controller function to update coach details
@bp.route('/coach/update', methods=['POST'])
def update_coach_details():
    try:
        data = request.get_json()
        email = data.get('email')
        coach_name = data.get('coach_name')
        domains = data.get('domains')
        coach_rating = data.get('coach_rating')
        coach_charges = data.get('coach_charges')
        coach_currency = data.get('coach_currency')
        coach_available = data.get('coach_available')

        coach = Coach.query.filter_by(email=email).first()
        if coach:
            coach.coach_name = coach_name
            coach.domains = domains
            coach.coach_rating = coach_rating
            coach.coach_charges = coach_charges
            coach.coach_currency = coach_currency
            coach.coach_available = coach_available
            db.session.commit()
            return jsonify({"message": "Coach details updated successfully", "coach": coach.to_dict()}), 200
        else:
            return jsonify({"error": "Coach with this email does not exist"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# Controller function to get all coaches
@bp.route('/coaches', methods=['GET'])
def get_coaches():
    try:
        coaches = Coach.query.all()
        if coaches:
            return jsonify({"coaches": [coach.to_dict() for coach in coaches]}), 200
        else:
            return jsonify({"message": "No coaches found"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# Controller function to get coaches by sport ID
@bp.route('/coaches/sport/<sport_id>', methods=['GET'])
def get_coaches_by_sport_id(sport_id):
    try:
        coaches = Coach.query.filter(Coach.domains.like(f'%{sport_id}%')).all()
        if coaches:
            return jsonify({"coaches": [coach.to_dict() for coach in coaches]}), 200
        else:
            return jsonify({"message": "No coaches found for this sport"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# Controller function to get coach details by coach ID
@bp.route('/coach/<coach_id>', methods=['GET'])
def get_coach_details_by_coach_id(coach_id):
    try:
        coach = Coach.query.get(coach_id)
        if coach:
            return jsonify({"coach": coach.to_dict()}), 200
        else:
            return jsonify({"message": "Coach not found"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# Controller function to toggle coach availability
@bp.route('/coach/availability/<coach_id>', methods=['POST'])
def toggle_availability(coach_id):
    try:
        data = request.get_json()
        available = data.get('available')

        if not isinstance(available, bool):
            return jsonify({"error": "Invalid availability value. It should be a boolean."}), 400

        coach = Coach.query.get(coach_id)
        if coach:
            coach.coach_available = available
            db.session.commit()
            return jsonify({"message": "Coach availability toggled successfully", "coach_id": coach.id, "new_availability": available}), 200
        else:
            return jsonify({"error": "Coach not found"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# Controller function to get available coaches
@bp.route('/coaches/available', methods=['GET'])
def get_available_coaches():
    try:
        coaches = Coach.query.filter_by(coach_available=True).all()
        if coaches:
            return jsonify({"coaches": [coach.to_dict() for coach in coaches]}), 200
        else:
            return jsonify({"message": "No available coaches found"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# Controller function to update coach rates
@bp.route('/coach/rates/update/<coach_id>', methods=['POST'])
def update_coach_rates(coach_id):
    try:
        data = request.get_json()
        currency = data.get('currency')
        charges = data.get('charges')

        coach = Coach.query.get(coach_id)
        if coach:
            coach.coach_currency = currency
            coach.coach_charges = charges
            db.session.commit()
            return jsonify({
                "message": "Coach rates updated successfully",
                "coach_id": coach.id,
                "currency": coach.coach_currency,
                "charges": coach.coach_charges
            }), 200
        else:
            return jsonify({"message": "Coach not found"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500


