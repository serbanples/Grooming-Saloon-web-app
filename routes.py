from flask import Flask, render_template, redirect, url_for
from flask import Blueprint

my_blueprint = Blueprint('my_blueprint', __name__)

#rute facute pe de-ampulea in afara de home page de care am zis ca ne ocupam acu

# Home Page
@my_blueprint.route('/')
def home():
    return render_template('index.html')

# User Authentication
@my_blueprint.route('/login')
def login():
    return render_template('login.html')

@my_blueprint.route('/register')
def register():
    return render_template('register.html')

@my_blueprint.route('/logout')
def logout():
    # Implement logout logic
    return 'Logout'

# Salon Management
@my_blueprint.route('/salons')
def list_salons():
    # Fetch and display a list of salons
    return render_template('salons.html')

@my_blueprint.route('/salon/<int:salon_id>')
def view_salon(salon_id):
    # Display details of a specific salon
    return render_template('salon_details.html', salon_id=salon_id)

# Appointment Booking
@my_blueprint.route('/book-appointment')
def book_appointment():
    # Display a form for booking appointments
    return render_template('book_appointment.html')

