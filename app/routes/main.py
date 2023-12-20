#repo/app/routes/main.py
from flask import render_template
from flask import Blueprint
from flask_login import login_manager

from app.routes import main  # Import my_blueprint from __init__.py

login_manager.login_view = 'auth.login'  # Set the login view for login_required

@main.route('/')
def home():
    return render_template('index.html')

# Salon Management
@main.route('/salons')
def list_salons():
    # Fetch and display a list of salons
    return render_template('salons.html')

@main.route('/salon/<int:salon_id>')
def view_salon(salon_id):
    # Display details of a specific salon
    return render_template('salon_details.html', salon_id=salon_id)

# Appointment Booking
@main.route('/book-appointment')
def book_appointment():
    # Display a form for booking appointments
    return render_template('book_appointment.html')
