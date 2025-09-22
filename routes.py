from flask import Blueprint, render_template, request, jsonify
from google.genai.types import GenerateContentConfig
from utility import isReview,getClient,is_rate_limited, db_write
from datetime import datetime
from model import *

review_bp = Blueprint("review_bp", __name__)

@review_bp.route("/")
def index():
    return render_template("index.html")

@review_bp.route("/generate-reply", methods=["POST"])
def generate_reply():
    user_ip = request.remote_addr
    if is_rate_limited(user_ip):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
    data = request.json
    review = data.get("review", "")
    tone = data.get("tone", "neutral")
    length = data.get("length", 50)
    instruction = data.get("instruction", "")
    
    if isReview(review):
        try:
            response = getClient().models.generate_content(
                model="gemini-2.5-flash-lite", 
                contents=f"you are professional customer support agent"
                f"acknowledge the specific issues mentioned, show understanding, provide thoughtful resolution"
                f"Write a {tone} business response to the following customer review in detail. "
                f"under {length} words."
                f"Do not include greetings, headers, or signatures."
                f"{instruction}"
                f"Review: {review}",
                config=GenerateContentConfig(
                    temperature=1,
                    candidate_count=1,
                    top_p=.9
                ),
            )
            #save to database
            user_to_add = User.query.filter_by(userIP=user_ip).first()
            review_to_add = Review.query.filter_by(content=review).first()
            reply_to_add = Review.query.filter_by(content=response.text).first()
            if not user_to_add:
                user_to_add = User(userIP=user_ip)
                db_write(user_to_add)
                
            if not review_to_add:
                review_to_add = Review(user_id=user_to_add.id,content=review)
                db_write(review_to_add)

            if not reply_to_add:
                reply_to_add = Review(user_id=user_to_add.id,parent_id=review_to_add.id,content=response.text)
                db_write(reply_to_add)

            return jsonify({"reply":response.text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "This input does not appear to be a customer review."}), 400

@review_bp.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    user_ip = request.remote_addr
    if is_rate_limited(user_ip):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
    data = request.json
    enjoy = data.get("enjoy")
    improvement = data.get("improvement", "")
    pay = data.get("pay")
    payment_type = data.get("payment_type", "")
    amount = data.get("amount", "")    

    feedback = {
        "ip": user_ip,
        "enjoy": enjoy,
        "improvement": improvement,
        "pay": pay,
        "payment_type": payment_type,
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    }

    # Save to database
    content = f"{enjoy},{pay},{amount},{improvement}"
    user_to_add = User.query.filter_by(userIP=user_ip).first()
    if not user_to_add:
        user_to_add = User(userIP=user_ip)
        db_write(user_to_add)
    feedback_to_add = Feedback.query.filter_by(user_id=user_to_add.id,feedback_text=content).first()
    if not feedback_to_add:
        feedback_to_add = Feedback(user_id=user_to_add.id,feedback_text=content)
        db_write(feedback_to_add)

    return jsonify({"success": True, "message": "Feedback submitted. Thank you!"}), 200