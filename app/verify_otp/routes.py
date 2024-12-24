from database.database import db
from model.otp_email import OtpEmail
from flask import Flask, request, jsonify
from . import bp
import random
import datetime 


def send_otp_email(email_id):
    otp = random.randint(100000,999999)
    new_otp = OtpEmail(email_id=email_id,otp_email=otp)
    db.session.add(new_otp)
    db.session.commit()

    print(f"OTP for {email_id} is {otp}")
    return otp



@bp.route("/send_otp_email",methods=["POST"])
def send_otp():
    data = request.get_json()
    email_id = data.get("email_id")

    if email_id:
        send_otp_email(email_id)
        return jsonify({"message": "OTP sent successfully"}), 200
    else:
        return jsonify({"message": "email_id is required"}), 400
    

@bp.route("/verify_email", methods=["POST"], endpoint="verify_email")
def verify_otp():
    data = request.get_json()
    email_id = data.get("email_id")
    otp_email = data.get("otp_email")

    valid_otp = OtpEmail.query.filter_by(email_id=email_id, otp_email=otp_email).first()
    if valid_otp:
        valid_time = datetime.datetime.utcnow() - valid_otp.created_at
        if valid_time.total_seconds() <= 120:

            db.session.delete(valid_otp)
            db.session.commit()
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "OTP has expired"}), 400
    else:
        return jsonify({"message": "Invalid OTP"}), 400






