import os
import requests
from models import Booking
from dotenv import load_dotenv

load_dotenv()

class PaymentRequest:
    
    @staticmethod
    def payment_creation(booking: Booking):

        url = (f"{os.getenv("PAYMENT_URL")}"
               f"/payment")
        
        payload = {
            "booking_id":Booking.id,
            "user_id":Booking.user_id,
            "amount":Booking.total_amount,
            "currency":Booking.currency
        }

        headers = {
            "X_API_KEY": os.getenv("API_KEY")
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=5
        )

        response.raise_for_status()

        return response.json()