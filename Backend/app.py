from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database import db
from dotenv import load_dotenv
from routes.auth import auth
from routes.event import event
from routes.booking import booking
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
    app.config['SECERET_KEY'] = f'{os.getenv("Key")}'
    app.config['JWT_SECRET_KEY'] = f'{os.getenv("Jkey")}'

    db.init_app
    JWTManager(app)
    CORS(app)

    app.register_blueprint(auth, url_prefix = "/auth")
    app.register_blueprint(event, url_prefix = "/event")
    app.register_blueprint(booking, url_prefix = "/booking")

    return app

if __name__ == "__main__":
    app = create_app
    with app.app_context():
        db.create_all()
    app.run(debug = True)