from flask import Blueprint, request, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import Event
from datetime import datetime

event = Blueprint("event", __name__)

@event.route('/Events', methods = ["GET"])
@jwt_required()
def events():
    page = request.args.get('page', 1, type = int)
    page_size = request.args.get('page_size', 5, type = int)

    events = Event.query.paginate(
        page = page,
        per_page = page_size,
        error_out = False
    )

    if not event:
        return jsonify({"message" : "No Event present To Book!"}), 404

    return jsonify({'total items': events.total,
                    'total_pages' : events.pages,
                    'current_page' : events.page,
                    'next_page' : events.has_next,
                    'previous_page' : events.has_prev,
                    'events': [e.to_dict() for e in events.items]}), 200

@event.route('/Events/AddEvent',  methods=["POST"])
@jwt_required()
def add_event():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    if claims["role"] != "organiser":
        return jsonify({"error" : "Your Not An Organiser To Add Events!"}), 403
    
    data = request.json

    if Event.query.filter_by(title = data["title"], event_time = datetime.strptime((data["date"]), "%Y-%m-%d %H:%M")).first():
        return jsonify ({"error" : "Event Already Exists!"}), 400

    event = Event(
        organiser_id = user_id,
        title = data["title"],
        description = data["description"],
        event_time = datetime.strptime(data["date"], "%Y-%m-%d %H:%M"),
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
    event.event_time = datetime.strptime(data.get("date", event.event_time), "%Y-%m-%d %H:%M")
    event.remaining_seats = int(data.get("seats", str(event.remaining_seats)))
 
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