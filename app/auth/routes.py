from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from model.session import Session
from model.athlete import Athlete
from model.coach import Coach
from model.wallet import Wallet 
from database.database import db
from . import bp
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_jwt_secret_key'
def generate_token(user_id):
    return jwt.encode(
        {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

# Routes
@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    user_type = data.get('user_type')

    if not email or not password or not confirm_password or not user_type:
        print(email,password,confirm_password,user_type)
        return jsonify({'error': 'Invalid input'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    if Session.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = None

    if user_type == 'athlete':
        new_user = Athlete(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        wallet = Wallet(athlete_id=new_user.id)
        db.session.add(wallet)

    elif user_type == 'coach':
        new_user = Coach(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    else:
        return jsonify({'error': 'Invalid user type'}), 400

    token = generate_token(new_user.id)
    session = Session(email=email, user_id=new_user.id, access_token=token, user_type=user_type)
    db.session.add(session)
    db.session.commit()

    return jsonify({'message': 'Registration successful', 'access_token': token, 'user_id': new_user.id})

@bp.route('/loging', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    session = Session.query.filter_by(email=email).first()
    if not session:
        return jsonify({'error': 'No account found with this email'}), 404

    user = None
    if session.user_type == 'athlete':
        user = Athlete.query.filter_by(email=email).first()
    elif session.user_type == 'coach':
        user = Coach.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': 'Login successful', 'access_token': session.access_token, 'user_id': user.id})
