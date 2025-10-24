from flask import Blueprint, request, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Booking
from models import Event

booking = Blueprint("booking", __name__)

@booking.route("/Bookings")
@jwt_required()
def show_bookings():
    user = get_jwt_identity()
    
    if user["role"] == "user":
        bookings = Booking.query.filter_by(user_id = user["id"])   
    elif user["role"] == "organiser":
        bookings = (
            Booking.query
            .join(Event, Booking.event_id == Event.id)
            .filter(Event.organiser_id == user["id"])
            .all()
            )
    return jsonify([b.to_dict() for b in bookings])

@booking.route("/Bookings/<int:id>", methods=["POST"])
@jwt_required()
def add_booking(id):
    user = get_jwt_identity()

    if user["role"] != "user":
        return jsonify({"error" : "Sorry You Cant Book Events"}), 403

    data = request.json
    event = Event.query.get(id)
    seats_booking = data.get("seats")

    if Booking.query.filter_by(event_id = id, user_id = user["id"]).first():
        return ({"error" : "You Already Have A Similar Booking!"}), 400
    
    if event.remaining_seats < seats_booking:
        return({"error" : f'Only {event.remaining_seats} seat are available'}), 404
    
    event.remaining_seats -= seats_booking

    booking = Booking(
        user_id = user["id"],
        event_id = data["event_id"],
        status = data["status"],
        seats = seats_booking
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify ({"message" : "Seats Booked Successfuly For The Event!",
                    "remaining_seats" : event.remaining_seats}), 200

@booking.route("/Bookings/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete_booking(id):
    user = get_jwt_identity()

    if user["role"] != "user":
        return jsonify({"error" : "Not an user!"}), 401
    
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error" : "Booking not found!"}), 404
    
    event = Event.query.get(booking.event_id)
    event.remaining_seats += booking.seats

    db.session.delete(booking)
    db.session.commit()

    return jsonify({"message" : "Booking cancelled successfully!"}), 200