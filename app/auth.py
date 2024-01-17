# repo/app/auth/auth.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user
from . import db, login_manager
from .models import User
import re

from flask import Blueprint

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')

        if not all([validate_name(first_name), validate_name(last_name), validate_email(email),
                    validate_password(password), validate_phone_number(phone_number)]):
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('auth.login'))

        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Account created successfully!')
        return redirect(url_for('main.home'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not all([validate_email(email), validate_password(password)]):
            flash('Invalid input. Please check your entries and try again.', 'error')
            return redirect(url_for('auth.login'))
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('main.home'))

        flash('Invalid email or password. Please try again.')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


def validate_name(name):
    if not name or not name.isalpha():
        flash('Invalid name. Please check your entries and try again.', 'error')
        return False
    return True


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Invalid email. Please check your entries and try again.', 'error')
        return False
    return True


def validate_password(password):
    if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) \
            or not re.search("[0-9]", password) or not re.search("[!@#$%^&*()]", password):
        flash('Password must be minimum 8 characters long and must contain lowercase and uppercase letters, numbers and special characters.', 'error')
        return False
    return True


def validate_phone_number(phone_number):
    if not re.match(r"^[0-9]{10}$", phone_number):
        flash('Invalid phone number. Please check your entries and try again.', 'error')
        return False
    return True
