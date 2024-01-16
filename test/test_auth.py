import os
import secrets
import unittest
from flask import Flask
from flask.testing import FlaskClient
from flask_login import LoginManager, current_user
from app import db
from app.models import User
from app.auth.auth import auth  # Import your auth blueprint here

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app.register_blueprint(auth, url_prefix='/auth')  # Register the auth blueprint

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.create_test_user()
            self.login_manager = LoginManager()
            self.login_manager.init_app(self.app)

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_user(self):
        with self.app.app_context():
            test_user = User(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                phone_number="1234567890"
            )
            test_user.set_password("Password@123")
            db.session.add(test_user)
            db.session.commit()

    def test_successful_login(self):
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a successful redirect
        self.assertEqual(response.location,
                         'http://localhost/')  # Assuming the successful login redirects to the home page
        self.assertTrue(current_user.is_authenticated)

    def test_unsuccessful_login(self):
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200)  # 200 is the status code for a successful login page render
        self.assertIn(b'Invalid email or password. Please try again.', response.data)
        self.assertFalse(current_user.is_authenticated)


if __name__ == '__main__':
    unittest.main()
