from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db



coach_services = db.Table(
    'coach_services',
    db.Column('coach_id', db.Integer, db.ForeignKey('coaches.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)

class Services(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)  
    # coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False) 
    services = db.Column(db.String(255), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

    


    def __init__(self,services):
    #     # self.coach_id = coach_id
        self.services = services

    def to_dict(self):
        """Serialize the object to a dictionary."""
        return {
            "id": self.id,
            # "coach_id": self.coach_id,
            "services": self.services,
            "label": self.services.title(),  
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            # "coach_ids": [coachs.id for coachs in self.coach]
        }
