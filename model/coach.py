from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from database.database import db


class Coach(db.Model):
    __tablename__ = 'coaches'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    coach_name = db.Column(db.String(255))
    coach_phone = db.Column(db.String(15))
    coach_dob = db.Column(db.String(20))
    coach_address = db.Column(db.Text)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    # domains = db.Column(db.ARRAY(db.Integer)) # Assuming domains are a list of Object IDs
    domains = db.Column(db.String(100))
    detail_experience = db.Column(db.Text)
    # coach_rating = db.Column(db.Float, default=0)
    # coach_languages = db.Column(db.ARRAY(db.String))
      # Storing as a list of strings
    coach_languages = db.Column(db.String(160)) 
    coach_age = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    # coach_charges = db.Column(db.Float, default=0)
    # coach_currency = db.Column(db.String(10))
    # coach_available = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    image =db.relationship("Image",backref="coach",lazy=True,)
    def __repr__(self):
        return f"<Coach {self.coach_name} ({self.email})>"


    def to_dict(self):
        return {
            "id": self.id,
            "coach_name": self.coach_name,
            "coach_phone": self.coach_phone,
            "coach_dob": self.coach_dob,
            "coach_address": self.coach_address,
            "email": self.email,
            "domains": self.domains,
            "detail_experience": self.detail_experience,
            # "coach_rating": self.coach_rating,
            "coach_languages": self.coach_languages,
            "coach_age": self.coach_age,
            "gender": self.gender,
            # "coach_charges": self.coach_charges,
            # "coach_currency": self.coach_currency,
            # "coach_available": self.coach_available,
            
            
        }
    
    @staticmethod
    def create_coach(payload):
        coach=Coach(
            coach_name=payload["coach_name"],
            coach_phone=payload["coach_phone"],
            coach_dob=payload["coach_dob"],
            coach_address=payload["coach_address"],
            email=payload["email"],
            password=payload["password"],
            domains=payload["domains"],
            detail_experience=payload["detail_experience"],
            # coach_rating=payload["coach_rating"],
            coach_languages=payload.get("coach_languages"),
            coach_age=payload.get("coach_age"),
            gender=payload.get("gender"),
            # coach_charges=payload["coach_charges"],
            # coach_currency=payload["coach_currency"],
            # coach_available=payload["coach_available"],
            created_at=payload["created_at"],
            updated_at=payload["updated_at"]

        )

        try:
            db.session.add(coach)
            db.session.commit()
            return True
        except IntegrityError:
            return False
    
     