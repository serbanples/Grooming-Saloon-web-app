#repo/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app.routes.main import main  # Import main blueprint
from app.auth.auth import auth  # Import auth_bp from auth

app.register_blueprint(main)  # Register the main blueprint
app.register_blueprint(auth, url_prefix='/auth')  # Register auth blueprint with a prefix

if __name__ == '__main__':
    app.run(debug=True)
