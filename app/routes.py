#repo/app/routes/routes.py
from flask import render_template
from flask import Blueprint
from flask_login import login_manager

main = Blueprint('main', __name__)
login_manager.login_view = 'auth.login'  # Set the login view for login_required

@main.route('/')
def home():
    return render_template('index.html')


