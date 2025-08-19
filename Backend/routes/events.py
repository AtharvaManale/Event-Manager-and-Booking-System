from flask import Blueprint, request, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Event

event = Blueprint("event", __name__)

@event.route('/events')
def events():
    events = Event.query.all()
    return jsonify ({e.to_dict() for e in events})

@event.route('/add')
@jwt_required
def add():
    user = get_jwt_identity()

    if user["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser To Add Events!"}), 403
    
    data = request.json

    if Event.query.filter_by(title = data["title"], date = data["date"]):
        return jsonify ({"error" : "Event Already Exists!"}), 400

    event = Event(
        title = data["title"],
        description = data["description"],
        date = data["date"],
        seats = data["seats"],
        organiser_id = user["id"]
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({"message" : "New Event Added Successfuly!"}), 201