from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(20), default = "user") #user or organiser

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id" : self.id,
            "username" : self.username,
            "role" : self.role
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    organiser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(150),unique= True, nullable = False)
    description = db.Column(db.Text, nullable = False)
    date_time = db.Column(db.DateTime, nullable = False)
    remaining_seats = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "date" : self.date_time,
            "remaining_seats" : self.remaining_seats,
            "organiser_id" : self.organiser_id
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable = False)
    seats = db.Column(db.Integer, nullable = False, default = 1)
    status = db.Column(db.String(20), default = 'Confirmed')

    def to_dict(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "event_id" : self.event_id,
            "seats" : self.seats,
            "status" : self.status
        }
