from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password_hash = db.Column(db.String(50), unique = True, nullable = False)
    role = db.column(db.String(20), default = "user") #user or organiser

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

class Event(db.model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(150),unique= True, nullable = False)
    description = db.Column(db.Text, nullable = False)
    date = db.Column(db.Date, nullable = False)
    seats = db.Column(db.Integer, nullable = False)
    organiser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "date" : self.date,
            "seats" : self.seats,
            "organiser_id" : self.organiser_id
        }

class Booking(db.model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.foreignKey('user.id'), nullable = False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable = False)
    status = db.Column(db.String(20), default = 'Booked')

    def to_dict(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "event_id" : self.event_id,
            "status" : self.status
        }

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)