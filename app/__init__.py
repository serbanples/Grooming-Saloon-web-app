#repo/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import secrets
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # + os.path.join(basedir, 'instance', 'site.db')

    with app.app_context():
        db.init_app(app)
        db.create_all()
        migrate = Migrate(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .salon_management import salon as salon_blueprint
    app.register_blueprint(salon_blueprint)

    from .appointment_management import appointment as appointment_blueprint
    app.register_blueprint(appointment_blueprint)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
