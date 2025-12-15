from flask import Blueprint, request, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import Event

event = Blueprint("event", __name__)

@event.route('/Events', methods = ["GET"])
@jwt_required()
def events():
    events = Event.query.all()
    if not event:
        return jsonify({"error" : "No Event present To Book!"}), 404

    return jsonify ([e.to_dict() for e in events]), 200

@event.route('/Events/AddEvent',  methods=["POST"])
@jwt_required()
def add_event():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser To Add Events!"}), 403
    
    data = request.json

    if Event.query.filter_by(title = data["title"], date_time = data["date"]).first():
        return jsonify ({"error" : "Event Already Exists!"}), 400

    event = Event(
        organiser_id = user_id,
        title = data["title"],
        description = data["description"],
        date_time = data["date"],
        remaining_seats = int(data["remaining_seats"])
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({"message" : "New Event Added Successfuly!"}), 200

@event.route('/Events/<int:id>', methods=["PUT"])
@jwt_required()
def update_event(id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser!"}), 403
    
    event = Event.query.get(id)
    if not event:
        return jsonify({"error" : "Event Not Found!"}), 404
    if event.organiser_id != user_id:
        return jsonify ({"error" : "Your Not The Organiser Of This Event!"}), 403

    data = request.json
    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.date_time = data.get("date", event.date_time)
    event.remaining_seats = data.get("seats", event.remaining_seats)
 
    db.session.commit()
    return jsonify({"message" : "Event updated successfuly!"}), 200

@event.route('/Events/<int:id>', methods = ["DELETE"])
@jwt_required()
def delete_event(id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser!"}), 403
    
    event = Event.query.get(id)
    if not event:
        return jsonify({"error" : "Event Not Found!"}), 404
    if event.organiser_id != user_id:
        return jsonify ({"error" : "Your Not The Organiser Of This Event!"}), 403
    
    db.session.delete(event)
    db.session.commit()

    return jsonify({"message" : "Event Successfuly Deleted!"}), 200