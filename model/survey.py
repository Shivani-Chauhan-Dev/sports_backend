from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    email = db.Column(db.String(255), nullable=False, unique=True)  # Unique and required email field
    budget = db.Column(db.String(255), nullable=False)  # Budget (required)
    charge_method = db.Column(db.String(255), nullable=False)  # Charge method (required)
    communication_method = db.Column(db.String(255), nullable=False)  # Communication method (required)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Default timestamp

    def __init__(self, email, budget, charge_method, communication_method):
        self.email = email
        self.budget = budget
        self.charge_method = charge_method
        self.communication_method = communication_method

    def to_dict(self):
        """Serialize the object to a dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "budget": self.budget,
            "charge_method": self.charge_method,
            "communication_method": self.communication_method,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
