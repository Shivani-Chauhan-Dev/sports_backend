from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os



class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    user_id = db.Column(db.Integer, nullable=False)  # Reference to User (Athlete or Coach)
    email = db.Column(db.String(255), nullable=False, unique=True)
    user_type = db.Column(db.Enum('athlete', 'coach', name='user_type_enum'), default='athlete')
    access_token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Instance method to compare passwords
    def compare_password(self, password):
        """Compare the provided password with the stored hashed password."""
        return check_password_hash(self.access_token, password)

    # Instance method to generate JWT token
    def generate_token(self):
        """Generate a JWT token for the session."""
        payload = {"id": self.id, "email": self.email}
        secret = os.getenv("JWT_SECRET", "default_secret")
        return jwt.encode(payload, secret, algorithm="HS256")

    # Override save behavior to hash the password if modified
    def save(self):
        """Hash the access token before saving."""
        if hasattr(self, 'access_token') and not self.access_token.startswith("$2b$"):
            self.access_token = generate_password_hash(self.access_token)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Session {self.email}>"
