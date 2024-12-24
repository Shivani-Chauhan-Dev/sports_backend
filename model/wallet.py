from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database.database import db

class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'), nullable=False)  # Foreign key referencing Athlete
    amount = db.Column(db.Float, default=0)  # Wallet amount with a default value of 0
    transactions = db.relationship('Transaction', backref='wallet', cascade='all, delete-orphan', lazy=True)  # Relationship to transactions

    def __init__(self, athlete_id, amount=0):
        self.athlete_id = athlete_id
        self.amount = amount

    def to_dict(self):
        """Serialize the Wallet object to a dictionary."""
        return {
            "id": self.id,
            "athlete_id": self.athlete_id,
            "amount": self.amount,
            "transactions": [transaction.to_dict() for transaction in self.transactions]
        }


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)  # Foreign key referencing Wallet
    amount = db.Column(db.Float, nullable=False)  # Transaction amount
    type = db.Column(db.String(10), nullable=False)  # Type of transaction ('credit' or 'debit')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Transaction timestamp

    def __init__(self, wallet_id, amount, type):
        self.wallet_id = wallet_id
        self.amount = amount
        self.type = type

    def to_dict(self):
        """Serialize the Transaction object to a dictionary."""
        return {
            "id": self.id,
            "wallet_id": self.wallet_id,
            "amount": self.amount,
            "type": self.type,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
