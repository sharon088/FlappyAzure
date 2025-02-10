import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app, users

REGISTER_ROUTE = "/register"
LOGIN_ROUTE = "/login"
LOGIN_MESSAGE = "Login succesful!"


class TestFlappyBirdApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        self.mock_users = MagicMock()
        users.find_one = self.mock_users.find_one
        users.insert_one = self.mock_users.insert_one
        users.delete_one = self.mock_users.delete_one

    def test_register_success(self):
        self.mock_users.find_one.return_value = None
        self.mock_users.insert_one.return_value = None
        response = self.client.post(
            REGISTER_ROUTE, json={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(LOGIN_MESSAGE, response.json["message"])
        self.mock_users.insert_one.assert_called_once_with(
            {"username": "testuser", "password": "testpassword"}
        )
        self.mock_users.find_one.assert_called_once_with({"username": "testuser"})

    def test_register_missing_username(self):
        response = self.client.post(REGISTER_ROUTE, json={"password": "testpassword"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username is required", response.json["error"])

    def test_register_invalid_username(self):
        response = self.client.post(
            REGISTER_ROUTE, json={"username": "123user", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username must contain only letters", response.json["error"])

    def test_login_success(self):
        self.mock_users.find_one.return_value = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(
            LOGIN_ROUTE, json={"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(LOGIN_MESSAGE, response.json["message"])
        self.mock_users.find_one.assert_called_once_with({"username": "testuser"})

    def test_login_unregistered_user(self):
        self.mock_users.find_one.return_value = None
        response = self.client.post(
            LOGIN_ROUTE, json={"username": "nonexistent", "password": "password"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username must be registerd", response.json["error"])

    def test_login_wrong_password(self):
        self.mock_users.find_one.return_value = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(
            LOGIN_ROUTE, json={"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("The password is wrong", response.json["error"])

    def test_register_extra_fields(self):
        self.mock_users.find_one.return_value = None
        self.mock_users.insert_one.return_value = None
        response = self.client.post(
            REGISTER_ROUTE,
            json={"username": "testuser", "password": "testpassword", "extra": "field"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(LOGIN_MESSAGE, response.json["message"])
        self.mock_users.insert_one.assert_called_once_with(
            {"username": "testuser", "password": "testpassword"}
        )
        self.mock_users.find_one.assert_called_once_with({"username": "testuser"})

    def test_register_empty_payload(self):
        response = self.client.post(REGISTER_ROUTE, json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username is required", response.json["error"])


if __name__ == "__main__":
    unittest.main()
