#repo/app/models.py
from flask_login import UserMixin
from . import db  # Import db instance from app.py
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # New field for admin status
    has_salons = db.Column(db.Boolean, default=False)  # New field for salon ownership
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', name="fk_salon_creator"), nullable=False)

    creator = db.relationship('User', backref=db.backref('created_salons', lazy=True))
    # Add more fields as needed

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_corresp_client'), nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id', name='fk_corresp_salon'), nullable=False)

    client = db.relationship('User', backref=db.backref('appointments', lazy=True))
    salon = db.relationship('Salon', backref=db.backref('appointments', lazy=True))