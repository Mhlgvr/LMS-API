import unittest
from src.routes_init import init_routes
from flask import Flask
from src.database import users, courses

class TestUsersAndCourses(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        init_routes(self.app)
        self.client = self.app.test_client()
        users.clear()
        courses.clear()

    def test_update_user(self):
        users[1] = {"user_id": 1, "login": "old_login", "first_name": "Old", "last_name": "User", "role": "student"}
        response = self.client.put(
            '/users/1',
            json={'user_id': 1, 'login': 'new_login', 'first_name': 'New', 'last_name': 'User', 'role': 'student'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "User updated successfully"})

    def test_update_user_not_found(self):
        response = self.client.put(
            '/users/12',
            json={'user_id': 12, 'login': 'new_login', 'first_name': 'New', 'last_name': 'User', 'role': 'student'}
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {'error': 'User not found'})

    def test_delete_user(self):
        users[1] = {"user_id": 1, "login": "test_user", "first_name": "Test", "last_name": "User", "role": "student"}
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "User deleted successfully"})

    def test_delete_user_not_found(self):
        response = self.client.delete('/users/12')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {'error': 'User not found'})

    def test_update_course(self):
        courses[1] = {"course_id": 1, "name": "Old Course", "description": "Old Description"}
        response = self.client.put(
            '/courses/1',
            json={'course_id': 1, 'name': 'New Course', 'description': 'New Description'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "Course updated successfully"})

    def test_update_course_not_found(self):
        response = self.client.put(
            '/courses/12',
            json={'course_id': 12, 'name': 'New Course', 'description': 'New Description'}
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {'error': 'Course not found'})

    def test_delete_course(self):
        courses[1] = {"course_id": 1, "name": "Test Course", "description": "Test Description"}
        response = self.client.delete('/courses/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "Course deleted successfully"})

    def test_delete_course_not_found(self):
        response = self.client.delete('/courses/12')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {'error': 'Course not found'})

if __name__ == '__main__':
    unittest.main()
