from flask import Flask, request, jsonify
from model.athlete import Athlete
from model.wallet import Wallet,Transaction
from database.database import db
from . import bp
from sqlalchemy.orm.exc import NoResultFound


@bp.route('/get_wallet_amount/<int:athlete_id>', methods=['GET'])
def get_wallet_amount(athlete_id):
    try:
        athlete = Athlete.query.get(athlete_id)
        if not athlete:
            return jsonify({'success': False, 'message': 'Athlete not found'}), 404

        wallet = Wallet.query.filter_by(athlete_id=athlete.id).first()
        if not wallet:
            return jsonify({'success': False, 'message': 'Wallet not found'}), 404

        return jsonify({'success': True, 'amount': wallet.amount}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to add money to the wallet
@bp.route('/add_money', methods=['POST'])
def add_money():
    try:
        data = request.get_json()
        athlete_id = data.get('athlete_id')
        amount = data.get('amount')

        athlete = Athlete.query.get(athlete_id)
        if not athlete:
            return jsonify({'success': False, 'message': 'Athlete not found'}), 404

        wallet = Wallet.query.filter_by(athlete_id=athlete.id).first()
        if not wallet:
            wallet = Wallet(athlete_id=athlete.id)
            db.session.add(wallet)

        wallet.amount += amount

        # Create a new transaction
        transaction = Transaction(
            # id=str(uuid.uuid4()),
            # transaction_id=str(db.session.get_bind()._get_current_connection().connection_id),  # Generate a unique transaction ID
            amount=amount,
            type="credit" if amount > 0 else "debit",
            wallet_id=wallet.id
        )

        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Amount added successfully',
            'new_balance': wallet.amount
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# Route to get wallet transactions
@bp.route('/get_wallet_transactions/<int:athlete_id>', methods=['GET'])
def get_wallet_transactions(athlete_id):
    try:
        athlete = Athlete.query.get(athlete_id)
        if not athlete:
            return jsonify({'success': False, 'message': 'Athlete not found'}), 404

        wallet = Wallet.query.filter_by(athlete_id=athlete.id).first()
        if not wallet:
            return jsonify({'success': False, 'message': 'Wallet not found'}), 404

        transactions = Transaction.query.filter_by(wallet_id=wallet.id).all()

        return jsonify({
            'success': True,
            # 'transactions': [{'transaction_id': t.transaction_id, 'amount': t.amount, 'type': t.type} for t in transactions]
            'transactions': [{ 'amount': t.amount, 'type': t.type} for t in transactions]

        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
