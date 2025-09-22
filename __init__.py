from flask import Flask
from model import db
from os import environ
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('SQLALCHEMY_DATABASE_URI')
    print("SQLALCHEMY_DATABASE_URI:", environ.get('SQLALCHEMY_DATABASE_URI'))
    if not environ.get('SQLALCHEMY_DATABASE_URI'):
        raise RuntimeError("Database URL missing!")
    db.init_app(app)
    
    #create database tables
    with app.app_context():
        db.create_all()
        
    # Import and register routes
    from routes import review_bp
    app.register_blueprint(review_bp)

    return app
