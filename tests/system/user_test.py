"""System tests for API requests related to users.

Tests registration and login of users.
"""
from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(
                    '/register', data={'username':'testuser', 'password': '123##!'}
                )
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('testuser'))
                self.assertDictEqual(
                    json.loads(response.data),
                    {'message': 'User created successfully.'}
                )

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/register', data={'username':'testuser', 'password': '123##!'}
                )
                auth_response = client.post(
                    '/auth',
                    data=json.dumps({'username':'testuser', 'password': '123##!'}),
                    headers={'Content-Type': 'application/json'}
                )
                self.assertIn('access_token', json.loads(auth_response.data).keys())
        

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/register', data={'username':'testuser', 'password': '123##!'}
                )
                response = client.post(
                    '/register', data={'username':'testuser', 'password': '123##!'}
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(len(UserModel.query.filter_by(username='testuser').all()), 1)
                self.assertDictEqual(
                    json.loads(response.data),
                    {'message': 'A user with that username already exist.'}
                )
