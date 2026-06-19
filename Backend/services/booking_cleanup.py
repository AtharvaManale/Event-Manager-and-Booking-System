from models import Booking, Event
from database import db
from datetime import datetime, timedelta

class BookingCleanupService():

    @staticmethod
    def cleanup():
        timmer = datetime.utcnow() - timedelta(minutes=15)
        try:
            failed_bookings = Booking.query.filter(Booking.created_at < timmer, Booking.status == "PENDING_PAYMENT").all()
            if failed_bookings:
                for booking in failed_bookings:
                    event = Event.query.get(booking.event_id)
                    if event:
                        event.remaining_seats += booking.booked_seats
                    booking.status = "CANCELLED"
            
                db.session.commit()
            else:
                print("No Expired Bookings Present.")

        except Exception as e:
                db.session.rollback()
                print(f'Error : {e}')