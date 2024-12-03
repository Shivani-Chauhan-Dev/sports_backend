from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db

class Sport(db.Model):
    __tablename__ = 'sports'

    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    sport_name = db.Column(db.String(255), nullable=False, unique=True)  # Sport name (unique, required)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for updates

    def __init__(self, sport_name):
        self.sport_name = sport_name

    def to_dict(self):
        """Serialize the object to a dictionary."""
        return {
            "id": self.id,
            "sport_name": self.sport_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
