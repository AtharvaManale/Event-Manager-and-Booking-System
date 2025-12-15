from flask import Blueprint, request, jsonify
from database import db
from models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth = Blueprint("auth", __name__)

@auth.route('/', methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username = data["username"]).first():
        return jsonify ({"error" : "User Already Exists"}), 400
    
    user = User(username = data["username"], role = data.get("role", "user"))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message" : "SignUp Successfull!"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username = data["username"]).first()

    if not user or not user.check_password(data['password']):
        return jsonify ({"error" : "Incorrect Credentials!"}), 401

    token = create_access_token(identity= str(user.id), additional_claims={"role" : user.role})
    refresh_token = create_refresh_token(identity= str(user.id), additional_claims={"role" : user.role})

    return jsonify (
        {"message" : "Login Successfull!",
        "access_token": token,
        "refresh_token" : refresh_token}), 200

@auth.route('/refresh', methods=["POST"])
@jwt_required(refresh = True)
def New_refresh_token():
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)

    return jsonify({"message" : "New access_token generated successfully!", 
                    "access_token" : token}), 200

@auth.route('/delete_acc', methods = ["DELETE"])
@jwt_required()
def delete_acc():
    user = get_jwt_identity()
    acc = User.query.filter_by(id = user.get("id")).first()

    if not acc:
        return jsonify({"error" : "Account Not Found!"}), 404

    db.session.delete(acc)
    db.session.commit()

    return jsonify({"message" : "Account Deleted Successfuly!"}),200