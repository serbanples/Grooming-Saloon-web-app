# this will be used to create and view appointments for user

from flask_login import login_required, current_user
from . import db
from flask import Blueprint, render_template
from .models import Appointment, Salon

appointment = Blueprint('appointment', __name__)

def get_available_slots(salon_id):
    # Get all appointments for the given salon
    appointments = Appointment.query.filter_by(salon_id=salon_id).all()

    # Create a list of all possible time slots between 7:00 and 19:00
    all_slots = list(range(7, 19))

    # Iterate over the list of appointments
    for appointment in appointments:
        # Get the hour of the appointment
        appointment_hour = appointment.hour

        # Remove the appointment hour from the list of all slots
        if appointment_hour in all_slots:
            all_slots.remove(appointment_hour)

    # The remaining slots in the list are the available slots
    return all_slots

@appointment.route('/<int:salon_id>', methods=['GET'])
def salon_view(salon_id):
    salon = Salon.query.get(salon_id)
    available_slots = get_available_slots(salon_id)
    return render_template('salon_details.html', salon=salon, available_slots=available_slots)

# function that will be accessible from the salon_view page to book an appointment for that salon.
# frontend will provide user with the available slots to choose from. user will be logged in
# his details will be fetched from the database and the appointment will be created with the user id and salon id

@appointment.route('/<int:salon_id>/book-appointment', methods=['POST'])
@login_required
def book_appointment(salon_id, selected_hour):
    # Check if the user is logged in
    if not current_user.is_authenticated:
        return "User not logged in. Please log in to book an appointment."

    # Get the logged-in user's details from the database
    user_id = current_user.id  # Assuming the User model has an 'id' field

    # Check if the selected hour is valid (based on available slots)
    available_slots = get_available_slots(salon_id)  # Assuming you have the get_available_slots function
    if selected_hour not in available_slots:
        return "Invalid appointment time. Please choose a valid time slot."

    # Create the appointment
    new_appointment = Appointment(user_id=user_id, salon_id=salon_id, hour=selected_hour)

    # Save the appointment to the database
    db.session.add(new_appointment)
    db.session.commit()

    return f"Appointment booked successfully at {selected_hour}:00."

@appointment.route('/view-appointments')
@login_required
def view_appointments():
    # Get the logged-in user's details from the database
    user_id = current_user.id

    # Get all the appointments for the user
    appointments = Appointment.query.filter_by(user_id=user_id).all()

    return render_template('appointments.html', appointments=appointments)