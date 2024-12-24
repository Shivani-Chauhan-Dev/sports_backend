from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
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
    detail_health = db.Column(db.Text)
    # alternative_contact = db.Column(db.String(15))
    # health_height_desc = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Athlete {self.name} ({self.email})>"
    
    @staticmethod
    def create_athlete(payload):
        athlete=Athlete(
            email= payload["email"],
            password= payload["password"],
            phone= payload["phone"],
            name= payload["name"],
            dob= payload["dob"],
            address= payload["address"],
            detail_health=payload["detail_health"],
            # alternative_contact=payload["alternative_contact"],
            # health_height_desc=payload["health_height_desc"],
            created_at= payload["created_at"],
            updated_at= payload["updated_at"]
            
        )  

        try:
            db.session.add(athlete)
            db.session.commit() 
            return True
        except IntegrityError:
            return False

