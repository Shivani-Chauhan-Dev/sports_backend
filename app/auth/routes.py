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
from datetime import datetime, timedelta
import random
import datetime
from dotenv import load_dotenv
import os
from functools import wraps




# genratye token
# secret_key="this is secret"
secret_key = os.getenv("SECRET_KEYS", 'default-secret-key')

app = Flask(__name__)
app.config['secret_key'] = secret_key
serializer = URLSafeTimedSerializer(app.config['secret_key'])

def token_required(f):
    @wraps(f)
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
        

@bp.route("/reset_password", methods=["POST"], endpoint="reset_password")

def reset_password():
    data = request.get_json()
    phone = data.get("phone")
    email = data.get("email")
    password = data.get("password")
    is_coach=data.get("is_coach")

    
    user = None
    if is_coach==True:
        if phone:
            user = Coach.query.filter_by(phone=phone).first()
        elif email:
            user = Coach.query.filter_by(email=email).first()
    else:
        if email:
            # Retrieve user from the database by email
            user=Athlete.query.filter_by(email=email).first()
        elif phone:
            user = Athlete.query.filter_by(phone=phone).first()
                

    if user:
        hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                ).decode("utf-8")

        # Update user's password
        user.password=hashed_password
        db.session.commit()
        return jsonify({"message": "Password reset successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404







@bp.route("/get_services/<string:domains>",methods=["GET"])
def get_service(domains):
    try:
        services=Coach.query.filter_by(domains=domains)
        getservice=services.all()

        output=[]
        for allservice in getservice:
            ratings =  Review.query.filter_by(coach_id=allservice.id).all()
            # avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            

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
    









def generate_sample_data():
    """Generate sample earnings data for the week."""
    # Sample data points for each day (high and low ranges)
    daily_ranges = {
        'SUN': (400, 580),
        'MON': (400, 550),
        'TUE': (250, 550),
        'WED': (280, 380),
        'THU': (30, 400),
        'FRI': (30, 200),
        'SAT': (50, 320)
    }
    
    # Generate two series of data (as shown in the pink and red lines)
    series1 = []
    series2 = []
    
    # Get current date and calculate the start of the week (Sunday)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday() + 1)
    
    for i, (day, (min_val, max_val)) in enumerate(daily_ranges.items()):
        date = start_of_week + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        
        series1.append({
            'date': date_str,
            'day': day,
            'value': round(random.uniform(min_val * 0.8, max_val * 0.8), 2)
        })
        
        series2.append({
            'date': date_str,
            'day': day,
            'value': round(random.uniform(min_val, max_val), 2)
        })
    
    return {
        'lower_series': series1,
        'upper_series': series2
    }

@bp.route('/api/earnings', methods=['GET'])
def get_earnings():
    """API endpoint to get weekly earnings statistics."""
    try:
        data = generate_sample_data()
        return jsonify({
            'status': 'success',
            'data': data,
            'graphdata': {
                'generated_at': datetime.now().isoformat(),
                'period': 'weekly'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/earnings/<day>', methods=['GET'])
def get_earnings_by_day(day):
    """API endpoint to get earnings statistics for a specific day."""
    try:
        day = day.upper()
        if day not in ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']:
            return jsonify({
                'status': 'error',
                'message': 'Invalid day. Please use three-letter day abbreviation.'
            }), 400
            
        data = generate_sample_data()
        day_data = {
            'lower_series': next(item for item in data['lower_series'] if item['day'] == day),
            'upper_series': next(item for item in data['upper_series'] if item['day'] == day)
        }
        
        return jsonify({
            'status': 'success',
            'data': day_data,
            'graphdata': {
                'generated_at': datetime.now().isoformat(),
                'period': 'daily'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500



# @bp.route("/user/login", methods=["POST"])
# def user_login():
#     data = request.get_json()

#     if not data or not data.get("email") or not data.get("password"):
#         return jsonify({"message": "Email and password are required"}), 400

#     email = data["email"]
#     password = data["password"]

#     user = None
#     role = None


#     user = Coach.query.filter_by(email=email).first()
#     if user:
#         role = "coach"

#     # If not found in Coach, check Athlete
#     if not user:
#         user = Athlete.query.filter_by(email=email).first()
#         if user:
#             role = "athlete"

#     # If user not found in both
#     if not user:
#         return jsonify({"message": "Invalid email or password"}), 401

#     # Validate password
#     if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
#         return jsonify({"message": "Invalid email or password"}), 401

#     # Generate JWT token
#     token_payload = {
#         "id": user.id,
#         "role": role,
#         "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
#     }
#     token = jwt.encode(token_payload, secret_key, algorithm="HS256")

#     return jsonify({
#         "message": "Login successful",
#         "token": token,
#         "user": {
#             "id": user.id,
#             "role": role,
#             "email": user.email,
#             "name": getattr(user, "coach_name", getattr(user, "name", ""))  # coach_name for Coach, name for Athlete
#         }
#     }), 200



@bp.route("/me", methods=["GET"])
@token_required
def get_current_user():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split()[1] if auth_header else None

    if not token:
        return jsonify({"message": "Token is missing"}), 401

    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = decoded_token.get("id")
        role = decoded_token.get("role")

        if role == "coach":
            user = Coach.query.get(user_id)
        elif role == "athlete":
            user = Athlete.query.get(user_id)
        else:
            return jsonify({"message": "Invalid role in token"}), 401

        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"user": user.to_dict()}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401
