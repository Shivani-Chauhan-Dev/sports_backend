from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model.session import Session
from model.athlete import Athlete
from model.coach import Coach
from model.wallet import Wallet 
from database.database import db
from . import bp
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from itsdangerous import URLSafeTimedSerializer
import datetime
from model.review import Review


# genratye token
secret_key="this is secret"
app = Flask(__name__)
app.config['secret_key'] = secret_key
serializer = URLSafeTimedSerializer(app.config['secret_key'])

def token_required(f):
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        if auth_header:
            try:
                token = auth_header.split()[1]
            except IndexError:
                return jsonify({'error': 'Token format is invalid'}), 400
        else:
            return jsonify({'error':'Token is missing'}), 403

        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
           return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)

    return decorated



# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_jwt_secret_key'
# def generate_token(user_id):
#     return jwt.encode(
#         {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
#         app.config['SECRET_KEY'],
#         algorithm='HS256'
#     )

# # Routes
# @bp.route('/signup', methods=['POST'])
# def signup():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')
#     confirm_password = data.get('confirm_password')
#     user_type = data.get('user_type')

#     if not email or not password or not confirm_password or not user_type:
#         print(email,password,confirm_password,user_type)
#         return jsonify({'error': 'Invalid input'}), 400

#     if password != confirm_password:
#         return jsonify({'error': 'Passwords do not match'}), 400

#     if Session.query.filter_by(email=email).first():
#         return jsonify({'error': 'Email already exists'}), 400

#     hashed_password = generate_password_hash(password)
#     new_user = None

#     if user_type == 'athlete':
#         new_user = Athlete(email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         wallet = Wallet(athlete_id=new_user.id)
#         db.session.add(wallet)

#     elif user_type == 'coach':
#         new_user = Coach(email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#     else:
#         return jsonify({'error': 'Invalid user type'}), 400

#     token = generate_token(new_user.id)
#     session = Session(email=email, user_id=new_user.id, access_token=token, user_type=user_type)
#     db.session.add(session)
#     db.session.commit()

#     return jsonify({'message': 'Registration successful', 'access_token': token, 'user_id': new_user.id})

# @bp.route('/loging', methods=['POST'])
# def login():
#     data = request.json
#     email = data.get('email')
#     password = data.get('password')

#     session = Session.query.filter_by(email=email).first()
#     if not session:
#         return jsonify({'error': 'No account found with this email'}), 404

#     user = None
#     if session.user_type == 'athlete':
#         user = Athlete.query.filter_by(email=email).first()
#     elif session.user_type == 'coach':
#         user = Coach.query.filter_by(email=email).first()

#     if not user or not check_password_hash(user.password, password):
#         return jsonify({'error': 'Invalid email or password'}), 401

#     return jsonify({'message': 'Login successful', 'access_token': session.access_token, 'user_id': user.id})


@bp.route("/logging",methods=["POST"])
def logging():
    data = request.get_json()
    if data:
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        is_coach = data.get("is_coach")
        print(email,password)

        if (email or phone) and password :
            user = None
            if is_coach==True:
                if email:
                    user=Coach.query.filter_by(email=email).first()
                elif phone:
                    user = Coach.query.filter_by(phone=phone).first()
            
            else:
                if email:
                    user=Athlete.query.filter_by(email=email).first()
                elif phone:
                    user = Athlete.query.filter_by(phone=phone).first()

            if user:

                if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                
                    token = jwt.encode({'user': user.email if email else user.phone,'id': user.id, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=3600)}, app.config['secret_key'])
                    return jsonify(token)
                    # return jsonify({"message": "Login successful"}), 200
                else:
                    return jsonify({"message": "Invalid email or password"}), 401
            else:
                return jsonify({"message": "Missing email or password"}), 400
        else:
            return jsonify({"message": "No data provided"}), 400


@bp.route("/get_services/<string:domains>",methods=["GET"])
def get_service(domains):
    try:
        services=Coach.query.filter_by(domains=domains)
        getservice=services.all()

        output=[]
        for allservice in getservice:
            ratings =  Review.query.filter_by(coach_id=allservice.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            

            service_data = {
                "id":allservice.id,
                'coach_name': allservice.coach_name,
                "email":allservice.email,
                "coach_phone":allservice.coach_phone,
                # "location":allservice.location,
                # 'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'

            }
            output.append(service_data)
        return jsonify({"services":output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    






