from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    athlete = db.relationship('Athlete', backref=db.backref('chat_athletes', lazy=True))
    coach = db.relationship('Coach', backref=db.backref('chat_coaches', lazy=True))

    def __repr__(self):
        return f"<Chat Athlete {self.athlete_id} Coach {self.coach_id}>"

class ChatHistory(db.Model):
    __tablename__ = 'chat_histories'

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False) # No ForeignKey, but still need a column for the join condition
    chats = db.relationship('Chat', backref='history', lazy=True)

    def __repr__(self):
        return f"<ChatHistory {self.id}>"
