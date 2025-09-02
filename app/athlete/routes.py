from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import datetime
from model.athlete import Athlete
from database.database import db
from app.auth.routes import token_required,secret_key
from . import bp
import bcrypt
import jwt



@bp.route('/update_athlete', methods=['PUT'],endpoint="update_athlete")
@token_required
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
            # existing_athlete.created_at = datetime.utcnow()  # Update the creation time

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

@bp.route('/get_all_athletes', methods=['GET'],endpoint="get_athelete")
@token_required
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
    



@bp.route('/registration',methods=["POST"])
def create_new_athletes():
    current_date=str(datetime.datetime.now())
    data= request.get_json()
    if data:
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        phone = data.get('phone')
        dob = data.get('dob')
        address = data.get('address')
        detail_health = data.get('detail_health')
        # alternative_contact = data.get('alternative_contact')
        # health_height_desc = data.get('health_height_desc')
        created_at=current_date
        updated_at=current_date
        

        if email and password and name and phone and dob and address  and detail_health:
            existing_user= Athlete.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                ).decode("utf-8")

                if Athlete.create_athlete(
                        {
                        
                        "email":email,
                        "password":hashed_password,
                        "name":name,
                        "phone":phone,
                        "dob":dob,
                        "address":address,
                        "detail_health":detail_health,
                        # "alternative_contact":alternative_contact,
                        # "health_height_desc":health_height_desc,
                        "created_at":created_at,
                        "updated_at":created_at

                    }
                ):
                    return jsonify({"message": "Athlete created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create athlete"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400 


@bp.route("/atheleteprofile", methods=["PUT"], endpoint="edit_athelete_profile")
@token_required
def edit_athelete_profile():
    current_date=str(datetime.datetime.now())
    auth_header = request.headers.get('Authorization')
    payload = auth_header.split(" ")[1]
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])

    athelete_id = token["id"]
    atheletes = Athlete.query.get(athelete_id)

    if atheletes:
        data=request.get_json()
        if data.get("email") != "":
            atheletes.email = data.get("email", atheletes.email)
        if data.get("name") != "":
            atheletes.name = data.get("name", atheletes.name)
        if data.get("phone") != "":
            atheletes.phone = data.get("phone", atheletes.phone)
        if data.get("dob") != "":
            atheletes.dob = data.get("dob", atheletes.dob)
        if data.get("address") != "":
            atheletes.address = data.get("address", atheletes.address)
        if data.get("detail_health") != "":
            atheletes.detail_health = data.get("detail_health",atheletes.detail_health)
        if data.get("password") != "":
            password = data.get("password")
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8", "ignore"),
                bcrypt.gensalt()
            ).decode("utf-8")
            atheletes.password = hashed_password
        atheletes.lastupdated=current_date
        try:
            db.session.commit()
            return jsonify({"message": "athelete updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update user"}), 500
    else:
        return jsonify({"message": "athelete not found"}), 404


@bp.route("/atheleteprofile/<int:athlete_id>", methods=["GET"], endpoint="get_athlete_profile")
@token_required
def get_athlete_profile(athlete_id):
    """
    Fetch an athlete's profile by their ID.
    """
    try:
        athlete = Athlete.query.get(athlete_id)
        
        if athlete:
            athlete_data = {
                "id": athlete.id,
                "email": athlete.email,
                "name": athlete.name,
                "phone": athlete.phone,
                "dob": athlete.dob,
                "address": athlete.address,
                "detail_health": athlete.detail_health,
                
            }
            return jsonify({"athlete": athlete_data}), 200
        else:
            return jsonify({"message": "Athlete not found"}), 404

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching the athlete profile", "error": str(e)}), 500

