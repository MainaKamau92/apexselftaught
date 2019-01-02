import os
import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import *


class TestBase(TestCase):
    def create_app(self):
        # pass test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_TEST_URL')
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
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
        self.job_data = {
            'job_title': 'Software Engineering',
            'job_description': 'Software developer wanted',
            'job_requirements': 'Should be driven',
            'expected_pay': '100,000',
            'contact_email': 'newjob@test.com',
            'contact_number': '0710123456',
        }
        db.create_all()
    
    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
        
