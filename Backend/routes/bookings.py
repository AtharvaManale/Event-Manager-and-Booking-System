from flask import Blueprint, request, jsonify
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Booking

booking = Blueprint("booking", __name__)

@booking.route("/bookings")
def show_bookings():
    bookings = Booking.query.all()
    return jsonify([b.to_dict for b in bookings])

@booking.route("/addbooking", methods=["POST"])
@jwt_required
def add_booking():
    user = get_jwt_identity()

    if user["role"] != "user":
        return jsonify({"error" : "Sorry You Cant Book Events"}), 403
    
    data = request.json

    if Booking.query.filter_by(event_id = data["event_id"], user_id = user["id"]).first():
        return ({"error" : "You Already Have A Similar Booking!"}), 400
    
    booking = Booking(
        id = data["id"],
        user_id = user["id"],
        event_id = data["event_id"],
        status = data["status"]
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify ({"message" : "Seats Booked Successfuly For A New Event!"}), 200