from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """represents a user identified by ip address

    :param userIP: a user's ip address
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    userIP = db.Column(db.String(45), unique=True, nullable=False)

    reviews = db.relationship("Review", backref="user")
    feedbacks = db.relationship("Feedback", backref="user")


class Review(db.Model):
    """
    represents a user posted review

    :param user_id: the user who posts the review
    :param parent_id: the review
    :param cotent: review, or AI generated reply if parent_id not null
    """
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("reviews.id"), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    replies = db.relationship(
        "Review",
        backref=db.backref("parent", remote_side=[id]),
        cascade="all, delete-orphan"
    )


class Feedback(db.Model):
    """
    represents user feedback
    
    :param user_id: the user who posts the review
    :param feedback_text: the feedback
    """
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    feedback_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)