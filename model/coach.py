from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db


class Coach(db.Model):
    __tablename__ = 'coaches'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    coach_name = db.Column(db.String(255))
    coach_phone = db.Column(db.String(15))
    coach_dob = db.Column(db.Date)
    coach_address = db.Column(db.Text)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    domains = db.Column(db.ARRAY(db.Integer))  # Assuming domains are a list of Object IDs
    detail_experience = db.Column(db.Text)
    coach_rating = db.Column(db.Float, default=0)
    coach_languages = db.Column(db.ARRAY(db.String))  # Storing as a list of strings
    coach_charges = db.Column(db.Float, default=0)
    coach_currency = db.Column(db.String(10))
    coach_available = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Coach {self.coach_name} ({self.email})>"
