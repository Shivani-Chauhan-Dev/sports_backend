from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from model.athlete import Athlete
from database.database import db
from . import bp


@bp.route('/create_athlete', methods=['POST'])
def create_athlete():
    try:
        # Check if the user is an admin
        if 'role' not in session or session['role'] != 'admin':
            return jsonify({'error': 'Unauthorized: Only admins can create athletes.'}), 403

        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        dob = data.get('dob')
        address = data.get('address')
        alternative_contact = data.get('alternative_contact')
        health_height_desc = data.get('health_height_desc')

        email = session.get('email')  # Assuming email is stored in session

        # Check if an athlete with the same email already exists
        existing_athlete = Athlete.query.filter_by(email=email).first()
        if existing_athlete:
            return jsonify({'error': 'Athlete with this email already exists.'}), 400

        # Create a new athlete instance
        new_athlete = Athlete(
            email=email,
            name=name,
            phone=phone,
            dob=dob,
            address=address,
            alternative_contact=alternative_contact,
            health_height_desc=health_height_desc
        )

        # Save the athlete to the database
        db.session.add(new_athlete)
        db.session.commit()

        return jsonify({
            'message': 'Athlete created successfully',
            'athlete_id': new_athlete.id,
            'athlete': {
                'email': new_athlete.email,
                'name': new_athlete.name
            }
        }), 201
    except IntegrityError as e:
        db.session.rollback()  # Rollback the transaction in case of error
        return jsonify({'error': 'Integrity error: ' + str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Controller function to update athlete details
@bp.route('/update_athlete', methods=['PUT'])
def update_athlete_details():
    try:
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        name = data.get('name')
        dob = data.get('dob')
        address = data.get('address')
        alternative_contact = data.get('alternative_contact')
        health_height_desc = data.get('health_height_desc')

        # Find the athlete by email
        existing_athlete = Athlete.query.filter_by(email=email).first()

        if existing_athlete:
            # Update the athlete's details
            existing_athlete.phone = phone
            existing_athlete.name = name
            existing_athlete.dob = dob
            existing_athlete.address = address
            existing_athlete.alternative_contact = alternative_contact
            existing_athlete.health_height_desc = health_height_desc
            existing_athlete.created_at = datetime.utcnow()  # Update the creation time

            # Commit changes to the database
            db.session.commit()

            return jsonify({
                'message': 'Athlete details updated successfully',
                'athlete': {
                    'id': existing_athlete.id,
                    'email': existing_athlete.email,
                    'name': existing_athlete.name
                }
            }), 200
        else:
            return jsonify({'error': 'Athlete with this email does not exist'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Controller function to get all athletes
@bp.route('/get_all_athletes', methods=['GET'])
def get_all_athletes():
    try:
        athletes = Athlete.query.all()

        if not athletes:
            return jsonify({'msg': 'No athletes found'}), 404

        athlete_list = [{
            'id': athlete.id,
            'email': athlete.email,
            'name': athlete.name,
            'phone': athlete.phone,
            'dob': athlete.dob,
            'address': athlete.address
        } for athlete in athletes]

        return jsonify({'athletes': athlete_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500