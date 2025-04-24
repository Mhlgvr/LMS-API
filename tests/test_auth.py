import unittest
from src.auth import basic_auth_required
from flask import Flask
from src.database import users

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        users.clear()
        users[1] = {"login": "testuser", "password": "testpass", "role": "student"}

    def test_auth_success(self):
        @basic_auth_required
        def test_route():
            return "Success"

        with self.app.test_request_context("/test", headers={"Authorization": "Basic dGVzdHVzZXI6dGVzdHBhc3M="}):
            response = test_route()
            self.assertEqual(response, "Success")

    def test_auth_failure(self):
        @basic_auth_required
        def test_route():
            return "Success"

        # Определите маршрут /test
        @self.app.route("/test")
        @basic_auth_required
        def test():
            return "Success"

        with self.app.test_client() as client:
            response = client.get("/test", headers={"Authorization": "Basic invalid"})
            self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
