from flask import Flask
from flask import Blueprint
from database.database import db
from flask_cors import CORS
from app.coach import bp as coach_bp
from app.athlete import bp as athlete_bp
from app.sport import bp as sport_bp
from app.review import bp as review_bp
from app.survey import bp as survey_bp
from app.wallet import bp as wallet_bp
from app.chat import bp as chat_bp
from app.auth import bp as auth_bp
from app.verify_otp import bp as verify_otp_bp


# Function to create the Flask app
def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"
    app.config['SECRET_KEY'] = 'your_jwt_secret_key'

    CORS(app)

    # Configuring the database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:shivanichauhan@localhost:5000/apps"
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Create tables (if they don't exist)
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(coach_bp)
    app.register_blueprint(athlete_bp)
    app.register_blueprint(sport_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(survey_bp)
    app.register_blueprint(wallet_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(verify_otp_bp)
    return app  # Ensure the app is returned so it can be run

# Main block to run the app
if __name__ == '__main__':
    app = create_app()  # Create the app
    app.run(debug=True, port=5004)  # Run the app on port 5004
