from flask import Blueprint, request, jsonify
from database import db
from models import User
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__)

@auth.route('/')
def register():
    data = request.json
    if User.query.filter_by(username = data["username"]).first():
        return jsonify ({"error" : "User Already Exists"}), 400
    
    user = User(username = data["username"], role = data["role", "user"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message" : "Thanks For SigningUp!"})

@auth.route('/login')
def login():
    data = request.json
    user = User.query.filter_by(username = data["username"]).first()

    if not user or user.check_password(data['password']):
        return jsonify ({"error" : "Incorrect Credentials!"}), 
    
    token = create_access_token(identity={"id" : user.id, "role" : user.role})
    return jsonify ({"message" : "Login Successfull!"})