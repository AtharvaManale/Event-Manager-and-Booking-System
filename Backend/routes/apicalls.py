from flask import Blueprint, jsonify, request
from database import db
from models import Booking
from dotenv import load_dotenv
import os

load_dotenv()

internal = Blueprint("internal", __name__)


@internal.route('booking/<int:booking_id>/payment-created', methods = ['POST'])
def payment_created(booking_id):
    api_key = request.headers.get("X_API_KEY")

    if api_key != os.getenv("API_KEY"):
        return jsonify({"Error" : "Unauthorized!"}), 401

    booking = db.session.get(Booking, booking_id)
    
    if not booking:
        return jsonify({"error":"Booking doesn't exists!"}), 404
    
    data = request.json
    
    booking.payment_id = data["payment_id"]
    booking.payment_status = data["payment_status"]

    db.session.commit()

    return jsonify({"message": "Payment successfully created."})


@internal.route("bookings/<int:booking_id>/payment-confirmation", methods = ['POST'])
def payment_confirmed(booking_id):
    api_key = request.headers.get("X_API_KEY")

    if api_key != os.getenv("API_KEY"):
        return jsonify({"Error" : "Unauthorized!"}), 401
    
    booking = db.session.get(Booking, booking_id)

    if not booking:
        return jsonify({"error":"Booking doesn't exists!"}), 404
    
    if booking.status == "CONFIRMED":
        return jsonify({"message" : "Booking is already confirmed"}), 200
    
    data = request.json
    status = data["payment_status"]
    booking.payment_id = data["payment_id"]
    booking.payment_status = status

    if status == 'CAPTURED':
        booking.status = "CONFIRMED"

    elif status in ["FAILED", "EXPIRED"]:
        booking.status = "PAYMENT_PENDING"

    db.session.commit()

    return jsonify({"message" : "Booking confirmed successfully!"}), 200