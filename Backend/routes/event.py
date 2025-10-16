from flask import Blueprint, request, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Event

event = Blueprint("event", __name__)

@event.route('/events')
@jwt_required
def events():
    events = Event.query.all()
    if not event:
        return jsonify({"error" : "No Event present To Book!"}), 404

    return jsonify ([e.to_dict() for e in events])

@event.route('/addevent',  methods=["POST"])
@jwt_required
def add_event():
    user = get_jwt_identity()

    if user["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser To Add Events!"}), 403
    
    data = request.json

    if Event.query.filter_by(title = data["title"], date = data["date"]).first():
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

    return jsonify({"message" : "New Event Added Successfuly!"}), 200

@event.route('/events/<int:id>', methods=["PUT"])
@jwt_required()
def update_event(id):
    user = get_jwt_identity()
    if user["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser!"}), 403
    
    event = Event.query.get(id)
    if not event:
        return jsonify({"error" : "Event Not Found!"}), 404
    if event.organiser_id != user["id"]:
        return jsonify ({"error" : "Your Not The Organiser Of This Event!"}), 403

    data = request.json
    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.date = data.get("date", event.date)
    event.seats = data.get("seats", event.seats)

    db.session.commit()
    return jsonify({"message" : "Event updated successfuly!"}), 200

@event.route('/events/<int:id>', methods = ["DELETE"])
@jwt_required()
def delete_event(id):
    user = get_jwt_identity()
    if user["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser!"}), 403
    
    event = Event.query.get(id)
    if not event:
        return jsonify({"error" : "Event Not Found!"}), 404
    if event.organiser_id != user["id"]:
        return jsonify ({"error" : "Your Not The Organiser Of This Event!"}), 403
    
    db.session.delete(event)
    db.session.commit()

    return jsonify({"message" : "Event Successfuly Deleted!"}), 200