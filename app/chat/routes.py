from flask import Flask, request, jsonify
from model.chat import Chat
from database.database import db
from . import bp
from model.athlete import Athlete
from sqlalchemy.orm.exc import NoResultFound


@bp.route('/chat', methods=['POST'])
def create_chat():
    try:
        data = request.json
        new_chat = Chat(
            athlete_id=data['athlete_id'],
            coach_id=data['coach_id'],
            message=data['message']
        )
        db.session.add(new_chat)
        db.session.commit()
        return jsonify(success=True, chat={'id': new_chat.id, 'message': new_chat.message}), 201
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

# Get all history chats for a coach
@bp.route('/chats/coach/<int:coach_id>', methods=['GET'])
def get_coach_chats(coach_id):
    try:
        chats = Chat.query.filter_by(coach_id=coach_id).all()
        return jsonify(success=True, chats=[{'id': chat.id, 'message': chat.message, 'timestamp': chat.timestamp} for chat in chats]), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

# Get all history chats for an athlete
@bp.route('/chats/athlete/<int:athlete_id>', methods=['GET'])
def get_athlete_chats(athlete_id):
    try:
        chats = Chat.query.filter_by(athlete_id=athlete_id).all()
        return jsonify(success=True, chats=[{'id': chat.id, 'message': chat.message, 'timestamp': chat.timestamp} for chat in chats]), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

# Get all chats (Admin-only access can be added with authentication)
@bp.route('/chats', methods=['GET'])
def get_all_chats():
    try:
        chats = Chat.query.all()
        return jsonify(success=True, chats=[{'id': chat.id, 'message': chat.message, 'timestamp': chat.timestamp} for chat in chats]), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

# Get chat by ID
@bp.route('/chat/<int:chat_id>', methods=['GET'])
def get_chat_by_id(chat_id):
    try:
        chat = Chat.query.get(chat_id)
        if not chat:
            return jsonify(success=False, message="Chat not found"), 404
        return jsonify(success=True, chat={'id': chat.id, 'message': chat.message, 'timestamp': chat.timestamp}), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

# Delete chat by ID
@bp.route('/chat/<int:chat_id>', methods=['DELETE'])
def delete_chat_by_id(chat_id):
    try:
        chat = Chat.query.get(chat_id)
        if not chat:
            return jsonify(success=False, message="Chat not found"), 404
        db.session.delete(chat)
        db.session.commit()
        return jsonify(success=True, message="Chat deleted successfully"), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500
    
@bp.route("/chat/history", methods=["GET"])
def chat_history():
    athlete_id = request.args.get("athlete_id")
    coach_id = request.args.get("coach_id")

    if not athlete_id or not coach_id:
        return jsonify({"error": "Missing athlete_id or coach_id"}), 400

    chats = Chat.query.filter_by(
        athlete_id=athlete_id,
        coach_id=coach_id
    ).order_by(Chat.timestamp).all()

    return jsonify([
        {
            "id": chat.id,
            "message": chat.message,
            "timestamp": chat.timestamp.isoformat(),
            "sender": "athlete" if int(chat.athlete_id) == int(athlete_id) else "coach"
        } for chat in chats
    ])


@bp.route('/chat_list/<int:coach_id>', methods=['GET'])
def chat_list(coach_id):
    # Fetch athletes the coach has chatted with
    results = db.session.query(Athlete.id, Athlete.name).join(Chat, Chat.athlete_id == Athlete.id)\
        .filter(Chat.coach_id == coach_id).distinct().all()
    
    athletes = [{"id": a.id, "name": a.name} for a in results]
    return jsonify({"athletes": athletes}), 200
