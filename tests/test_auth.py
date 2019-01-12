from . import TestBase
from flask import url_for

class TestEmployer(TestBase):

    def test_user_registration(self):
        response_load = self.client.get(url_for('auth.register'))
        self.assertEqual(response_load.status_code, 200)
        url_response = self.client.get('/register/')
        response = self.client.post('/register/', data=self.user_data, follow_redirects=True)
        self.assertEqual(url_response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        
    
    def test_user_login(self):
        response_load = self.client.get(url_for('auth.login'))
        self.assertEqual(response_load.status_code, 200)
        url_response = self.client.get('/login/')
        response = self.client.post('/login/', data=self.login_data)
        self.assertEqual(url_response.status_code, 200)
        self.assertEqual(response.status_code, 200)

    
    def test_user_logout(self):
        response = self.client.post('/login/', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        redirect_url = url_for('auth.login', next=url_for('auth.logout'))
        response_logout = self.client.post('/logout/')
        self.assertEqual(response_logout.status_code, 302)
        self.assertRedirects(response_logout, redirect_url)

    def test_user_dashboard(self):
        response = self.client.post('/login/', data=self.login_data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/employer/dashboard')
        redirect_url = url_for('auth.login', next=url_for('employer.dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


