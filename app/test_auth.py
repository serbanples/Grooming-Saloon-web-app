import unittest
from flask_login import LoginManager, current_user

from . import db
from .models import User
from . import create_app


class AuthTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app()
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
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'Password@123'
        })
        self.assertEqual(response.status_code, 302)  # 302 is the status code for a successful redirect
        self.assertEqual(response.location,
                         'http://localhost/')  # Assuming the successful login redirects to the home page
        self.assertTrue(current_user.is_authenticated)

    def test_unsuccessful_login(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 302)  # 200 is the status code for a successful login page render
        self.assertIn(b'Invalid email or password. Please try again.', response.data)
        self.assertFalse(current_user.is_authenticated)


if __name__ == '__main__':
    unittest.main()
