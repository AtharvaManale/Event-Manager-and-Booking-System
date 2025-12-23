from flask import Blueprint, request, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import Booking
from models import Event

booking = Blueprint("booking", __name__)

@booking.route("/Bookings")
@jwt_required()
def show_bookings():
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    
    if claims["role"] == "user":
        bookings = Booking.query.filter_by(user_id = user_id)   
    elif claims["role"] == "organiser":
        bookings = (
            Booking.query
            .join(Event, Booking.event_id == Event.id)
            .filter(Event.organiser_id == user_id)
            .all()
            )
    return jsonify([b.to_dict() for b in bookings])

@booking.route("/Addbooking/<int:id>", methods=["POST"])
@jwt_required()
def add_booking(id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"error" : "Sorry You Cant Book Events"}), 403

    data = request.json
    event = Event.query.get(id)
    seats_booking = data.get("seats")

    if Booking.query.filter_by(event_id = id, user_id = user_id).first():
        return ({"error" : "You Already Have A Similar Booking!"}), 400
    
    if event.remaining_seats < seats_booking:
        return({"error" : f'Only {event.remaining_seats} seat are available'}), 409
    
    event.remaining_seats -= seats_booking

    booking = Booking(
        user_id = user_id,
        event_id = id,
        booked_seats = seats_booking
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify ({"message" : "Seats Booked Successfuly For The Event!",
                    "remaining_seats" : event.remaining_seats}), 200

@booking.route("/Deletebooking/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete_booking(id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims["role"] != "user":
        return jsonify({"error" : "Not an user!"}), 401
    
    booking = Booking.query.get(id)
    if not booking:
        return jsonify({"error" : "Booking not found!"}), 404
    
    event = Event.query.get(booking.event_id)
    event.remaining_seats += booking.booked_seats

    db.session.delete(booking)
    db.session.commit()

    return jsonify({"message" : "Booking cancelled successfully!"}), 200