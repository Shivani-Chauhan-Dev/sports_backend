from flask import Flask, request, jsonify
from model.athlete import Athlete
from model.survey import Survey
from database.database import db
from . import bp
from sqlalchemy.orm.exc import NoResultFound


@bp.route('/submit_survey', methods=['POST'])
def submit_survey():
    try:
        data = request.get_json()
        email = data.get('email')
        budget = data.get('budget')
        charge_method = data.get('charge_method')
        communication_method = data.get('communication_method')

        print(email,budget,charge_method,communication_method)
        # Check if athlete with the given email exists
        athlete = Athlete.query.filter_by(email=email).first()
        if not athlete:
            return jsonify({'success': False, 'message': 'Athlete not found'}), 404
        

        # Create a new survey entry
        survey = Survey(email=email, budget=budget, charge_method=charge_method, communication_method=communication_method)
        db.session.add(survey)
        db.session.commit()

        return jsonify({'success': True, 'survey': {'id': survey.id, 'email': survey.email, 'budget': survey.budget, 'chargeMethod': survey.charge_method, 'communicationMethod': survey.communication_method}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get a survey by email
@bp.route('/get_survey_by_email', methods=['GET'])
def get_survey_by_email():
    try:
        email = request.json.get('email')
        survey = Survey.query.filter_by(email=email).first()

        if not survey:
            return jsonify({'success': False, 'message': 'Survey not found'}), 404

        return jsonify({'success': True, 'survey': {'id': survey.id, 'email': survey.email, 'budget': survey.budget, 'chargeMethod': survey.charge_method, 'communicationMethod': survey.communication_method}}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get all surveys
@bp.route('/get_all_surveys', methods=['GET'])
def get_all_surveys():
    try:
        surveys = Survey.query.all()

        if not surveys:
            return jsonify({'success': False, 'message': 'No surveys found'}), 404

        return jsonify({'success': True, 'surveys': [{'id': survey.id, 'email': survey.email, 'budget': survey.budget, 'chargeMethod': survey.charge_method, 'communicationMethod': survey.communication_method} for survey in surveys]}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
