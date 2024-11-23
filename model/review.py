from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)  # Foreign key to Coach
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'), nullable=False)  # Foreign key to Athlete
    rating = db.Column(db.Float, nullable=False)  # Rating is required
    comment = db.Column(db.Text)  # Optional comment
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Default to current time

    # Relationships
    coach = db.relationship('Coach', backref=db.backref('reviews', lazy=True))
    athlete = db.relationship('Athlete', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f"<Review Coach {self.coach_id} Athlete {self.athlete_id} Rating {self.rating}>"
