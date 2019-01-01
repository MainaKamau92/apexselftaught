import unittest
import click
import os
from app import create_app, db

class TestEmployer(unittest.TestCase):

    def setUp(self):
        """
        Will be called before every test
        """
        config_name = 'testing'
        self.app = create_app(config_name)
       
        self.app.config.update(SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_TEST_URL'))
        self.client = self.app.test_client

        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'username': 'johndoe',
            'is_freelancer': False,
            'is_employer': True,
            'password': 'password123'
        }
        self.login_data = {
            'email': 'johndoe@test.com',
            'password': 'password123'
        }

        with self.app.app_context():
            # create all tables for the test database
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        url_response = self.client().get('/register/')
        response = self.client().post('/register/', data=self.user_data)
        self.assertEqual(url_response.status_code, 200)
        self.assertEqual(response.status_code, 200)
    
    def test_user_login(self):
        url_response = self.client().get('/login/')
        response = self.client().post('/login/', data=self.login_data)
        self.assertEqual(url_response.status_code, 200)
        self.assertEqual(response.status_code, 200)
    
    def test_user_logout(self):
        response = self.client().post('/login/', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        response_logout = self.client().post('/logout/')
        self.assertEqual(response_logout.status_code, 302)
    
    def test_user_dashboard(self):
        response = self.client().post('/login/', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/employer/dashboard')
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        """Tear down all initialized variables"""

        with self.app.app_context():
            # drop the tables
            db.session.remove()
            db.drop_all()
