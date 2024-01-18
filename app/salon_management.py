# this will be the endpoint for the salon creation by a user
from flask_login import login_required
from . import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Salon, User

salon = Blueprint('salon', __name__)

@salon.route('/create-salon', methods=['GET', 'POST']) # this requires a user to be logged in
@login_required
def create_salon():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        if not all([name, address]):
            flash('Invalid input. Please check your entries and try again.', 'error')
            return redirect(url_for('salon.create_salon'))
        new_salon = Salon(name=name, address=address)
        User.has_salons = True
        db.session.add(new_salon)
        db.session.commit()
        flash('Salon created successfully!')
        return redirect(url_for('main.home'))
    return render_template('create_salon.html')

@salon.route('/salons')
def list_salons():
    salons = Salon.query.all()
    return render_template('salons.html', salons=salons)