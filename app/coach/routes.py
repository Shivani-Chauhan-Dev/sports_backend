from flask import Flask, request, jsonify
from model.coach import Coach
import datetime
import bcrypt
from database.database import db
from . import bp
from sqlalchemy.orm.exc import NoResultFound
from app.auth.routes import token_required ,secret_key
# from model.services import Services
import jwt

@bp.route('/coach/update', methods=['PUT'])
def update_coach_details():
    try:
        data = request.get_json()
        email = data.get('email')
        coach_name = data.get('coach_name')
        coach_phone = data.get("coach_phone")
        coach_dob = data.get("coach_dob")
        coach_address = data.get("coach_address")
        domains = data.get('domains')
        detail_experience = data.get("detail_experience")
        # coach_rating = data.get('coach_rating')
        coach_languages = data.get("coach_languages")
        coach_age = data.get("coach_age")
        gender = data.get("gender")
        # coach_charges = data.get('coach_charges')
        # coach_currency = data.get('coach_currency')
        # coach_available = data.get('coach_available')

        coach = Coach.query.filter_by(email=email).first()
        if coach:
            coach.coach_name = coach_name
            coach.coach_phone = coach_phone
            coach.coach_dob = coach_dob
            coach.coach_address = coach_address
            coach.domains = domains
            coach.detail_experience = detail_experience
            # coach.coach_rating = coach_rating
            coach.coach_languages = coach_languages
            coach.coach_age = coach_age
            coach.gender = gender
            # coach.coach_charges = coach_charges
            # coach.coach_currency = coach_currency
            # coach.coach_available = coach_available
            db.session.commit()
            return jsonify({"message": "Coach details updated successfully", "coach": coach.to_dict()}), 200
        else:
            return jsonify({"error": "Coach with this email does not exist"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@bp.route('/coaches', methods=['GET'],endpoint="get_coaches")
@token_required  
def get_coaches():
    try:
        coaches = Coach.query.all()
        if coaches:
            return jsonify({"coaches": [coach.to_dict() for coach in coaches]}), 200
        else:
            return jsonify({"message": "No coaches found"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

#  get coaches by sport ID
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

# get coach details by coach ID
@bp.route('/coach/<coach_id>', methods=['GET'],endpoint="get_coach_id")
@token_required
def get_coach_details_by_coach_id(coach_id):
    try:
        coach = Coach.query.get(coach_id)
        if coach:
            return jsonify({"coach": coach.to_dict()}), 200
        else:
            return jsonify({"message": "Coach not found"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

# toggle coach availability
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

# get available coaches
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

#  update coach rates
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


@bp.route("/coachregistration",methods=["POST"])
def coach_registration():
    current_date=str(datetime.datetime.now())
    data = request.get_json()
    if data:
        coach_name = data.get("coach_name")
        coach_phone = data.get("coach_phone")
        coach_dob = data.get("coach_dob")
        coach_address = data.get("coach_address")
        email = data.get("email")
        password = data.get("password")
        domains = data.get("domains")
        detail_experience = data.get("detail_experience")
        # coach_rating = data.get("coach_rating")
        # coach_charges = data.get("coach_charges")
        # coach_currency = data.get("coach_currency")
        # coach_available = data.get("coach_available")
        created_at = current_date
        updated_at = current_date

        if coach_name and coach_phone and coach_dob and coach_address and email and password and domains and detail_experience:
            # print(email)
            existing_user= Coach.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt(14)
                ).decode("utf-8")

                if Coach.create_coach(
                    {
                        "coach_name":coach_name,
                        "coach_phone":coach_phone,
                        "coach_dob":coach_dob,
                        "coach_address":coach_address,
                        "email":email,
                        "password":hashed_password,
                        "domains":domains,
                        "detail_experience":detail_experience,
                        # "coach_rating":coach_rating,  
                        # "coach_charges":coach_charges,
                        # "coach_currency":coach_currency,
                        # "coach_available":coach_available,
                        "created_at":current_date,
                        "updated_at":current_date,


                    }
                ):
                    return jsonify({"message": "coach created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create coach"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}), 



# @bp.route("/coachregistration", methods=["POST"])
# def coach_registration():
#     current_date=str(datetime.datetime.now())
#     data = request.get_json()

#     # Validation
#     required_fields = ["coach_name", "coach_phone", "coach_dob", "coach_address", "email", "password", "domains", "detail_experience"]
#     if not data or not all(data.get(field) for field in required_fields):
#         return jsonify({"message": "Missing fields"}), 400

#     if Coach.query.filter_by(email=data["email"]).first():
#         return jsonify({"message": "User already exists"}), 400

#     # Create new coach
#     hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt(14)).decode("utf-8")
#     new_coach = Coach(
#         coach_name=data["coach_name"],
#         coach_phone=data["coach_phone"],
#         coach_dob=data["coach_dob"],
#         coach_address=data["coach_address"],
#         email=data["email"],
#         password=hashed_password,
#         detail_experience=data["detail_experience"],
#         created_at=current_date,
#         updated_at=current_date
#     )

#     db.session.add(new_coach)
#     db.session.flush()

#     cleaned_service = data["domains"].strip().lower()
#     service = Services.query.filter_by(services=cleaned_service).first()

#     # for service_name in data["domains"]:
#     #     cleaned_service = service_name.strip().lower()
#     #     service = Services.query.filter_by(services=cleaned_service).first()

#     if not service:
#         service = Services(services=cleaned_service)
#         db.session.add(service)
#         db.session.flush()

#     new_coach.services.append(service)

#     db.session.commit()
#     return jsonify({"message": "Coach registered successfully"}), 201

                    
                    
@bp.route("/profile", methods=["PUT"], endpoint="edit_coach_profile")
@token_required
def edit_coach_profile():
    current_date=str(datetime.datetime.now())
    auth_header = request.headers.get('Authorization')
    payload = auth_header.split(" ")[1]
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])

    coach_id = token["id"]
    coach = Coach.query.get(coach_id)

    if coach:
        data=request.get_json()
        if data.get("email") != "":
            coach.email = data.get("email", coach.email)
        if data.get("coach_name") != "":
            coach.coach_name = data.get("coach_name", coach.coach_name)
        if data.get("coach_phone") != "":
            coach.coach_phone = data.get("coach_phone", coach.coach_phone)
        if data.get("coach_dob") != "":
            coach.coach_dob = data.get("coach_dob", coach.coach_dob)
        if data.get("coach_address") != "":
            coach.coach_address = data.get("coach_address", coach.coach_address)
        if data.get("detail_experience") != "":
            coach.detail_experience = data.get("detail_experience",coach.detail_experience)
        if data.get("domains") != "":
            coach.domains = data.get("domains",coach.domains)
        if data.get("password") != "":
            password = data.get("password")
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8", "ignore"),
                bcrypt.gensalt()
            ).decode("utf-8")
            coach.password = hashed_password
        coach.lastupdated=current_date
        try:
            db.session.commit()
            return jsonify({"message": "coach updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update coach"}), 500
    else:
        return jsonify({"message": "coach not found"}), 404



# @bp.route("/profile", methods=["PUT"], endpoint="edit_coach_profile")
# @token_required
# def edit_coach_profile():
#     current_date = str(datetime.datetime.now())
#     auth_header = request.headers.get('Authorization')
#     payload = auth_header.split(" ")[1]
#     token = jwt.decode(payload, secret_key, algorithms=['HS256'])

#     coach_id = token["id"]
#     coach = Coach.query.get(coach_id)

#     if not coach:
#         return jsonify({"message": "coach not found"}), 404

#     data = request.get_json()

#     # Update coach fields
#     if data.get("email") != "":
#         coach.email = data.get("email", coach.email)
#     if data.get("coach_name") != "":
#         coach.coach_name = data.get("coach_name", coach.coach_name)
#     if data.get("coach_phone") != "":
#         coach.coach_phone = data.get("coach_phone", coach.coach_phone)
#     if data.get("coach_dob") != "":
#         coach.coach_dob = data.get("coach_dob", coach.coach_dob)
#     if data.get("coach_address") != "":
#         coach.coach_address = data.get("coach_address", coach.coach_address)
#     if data.get("detail_experience") != "":
#         coach.detail_experience = data.get("detail_experience", coach.detail_experience)
#     if data.get("password") != "":
#         password = data.get("password")
#         hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#         coach.password = hashed_password

#     # Handle domain (service) update
#     domains = data.get("domains", [])
#     if domains:
#         cleaned_service = domains.strip().lower()
#         # Clear old services
#         coach.services.clear()

#         # Add updated services

            
#         existing_service = Services.query.filter_by(services=cleaned_service).first()

#         if not existing_service:
#             existing_service = Services(services=cleaned_service)
#             db.session.add(existing_service)
#             db.session.flush()

#         coach.services.append(existing_service)

#     coach.lastupdated = current_date

#     try:
#         db.session.commit()
#         return jsonify({"message": "coach updated successfully"}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": f"Failed to update coach: {str(e)}"}), 500



@bp.route("/profile/<int:coach_id>", methods=["GET"], endpoint="get_coach_profile")
@token_required
def get_coach_profile(coach_id):
    
    try:
        coach = Coach.query.get(coach_id)
        if coach:
            coach_data = {
                "id": coach.id,
                "email": coach.email,
                "coach_name": coach.coach_name,
                "coach_phone": coach.coach_phone,
                "coach_dob": coach.coach_dob,
                "coach_address": coach.coach_address,
                "detail_experience": coach.detail_experience,
                "domains": coach.domains,
                
            }
            return jsonify({"coach": coach_data}), 200
        else:
            return jsonify({"message": "Coach not found"}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred while fetching the coach profile", "error": str(e)}), 500
    

# @bp.route('/get_coaches_by_service/<int:service_id>', methods=['GET'], endpoint='get_coaches_by_service')
# @token_required
# def get_coaches_by_service(service_id):
#     try:
#         service = Services.query.get(service_id)
#         if not service:
#             return jsonify({'success': False, 'message': 'Service not found'}), 404

#         coaches = service.coach 
#         coach_list = []
#         for coach in coaches:
#             coach_list.append({
#                 "id": coach.id,
#                 "coach_name": coach.coach_name,
#                 "coach_phone": coach.coach_phone,
#                 "coach_dob": coach.coach_dob,
#                 "coach_address": coach.coach_address,
#                 "email": coach.email,
#                 "detail_experience": coach.detail_experience
                
#             })

#         return jsonify({'success': True, 'coaches': coach_list}), 200

#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500










    


