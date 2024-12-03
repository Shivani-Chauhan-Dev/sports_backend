from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db

class Athlete(db.Model):
    __tablename__ = 'athletes'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255))
    phone = db.Column(db.String(15))
    name = db.Column(db.String(255))
    dob = db.Column(db.String(10))  # Can be changed to Date type if needed
    address = db.Column(db.Text)
    alternative_contact = db.Column(db.String(15))
    health_height_desc = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Athlete {self.name} ({self.email})>"
