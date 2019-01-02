from flask import url_for
from . import TestBase
import click

class TestEmployer(TestBase):

    def test_post_job(self):
        response = self.client.post('/login/', data=self.login_data)
        self.assertEqual(response.status_code, 200)   
        job_response = self.client.post('/employer/post/new', data=self.job_data)
        redirect_url = url_for('auth.login', next=url_for('employer.post_job'))
        self.assertEqual(job_response.status_code, 302)
        self.assertRedirects(job_response, redirect_url)
    
    def test_get_jobs(self):
        response_load = self.client.get(url_for('employer.job_posts'))
        self.assertEqual(response_load.status_code, 302)
        response = self.client.get('/jobs')
        self.assertEqual(response.status_code, 302)
