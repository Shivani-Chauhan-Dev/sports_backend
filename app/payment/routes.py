# from flask import Flask,jsonify,request
# from app.coach import Coach
# from . import bp
# # import razorpay
# import os


# # razorpay_client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))

# @bp.route("/create_order", methods=["POST"])
# def create_order():
#     data = request.json
#     athlete_id = data["athlete_id"]
#     coach_id = data["coach_id"]
#     amount = int(float(data["amount"]) * 100)  # in paise

#     coach = Coach.query.filter_by(id=coach_id).first()
#     if not coach:
#         return jsonify({"error": "Coach not found"}), 404

#     # Send the entire amount to the coach
#     # order = razorpay_client.order.create({
#         "amount": amount,
#         "currency": "INR",
#         "payment_capture": 1,
#         "transfers": [
#             {
#                 # "account": coach.razorpay_account_id,
#                 "amount": amount,  # Full amount
#                 "currency": "INR",
#                 "notes": {"for": "coach payment"}
#             }
#         ]
#     })

#     return jsonify({
#         "order_id": order["id"],
#         # "razorpay_key_id": os.getenv("RAZORPAY_KEY_ID"),
#         "amount": amount
#     })
