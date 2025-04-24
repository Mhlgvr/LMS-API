import unittest
from src.routes_init import init_routes
from flask import Flask
from src.database import problems, courses

class TestProblems(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        init_routes(self.app)
        self.client = self.app.test_client()
        problems.clear()
        courses.clear()
        courses[1] = {"course_id": 1, "name": "Test Course", "description": "Test Description"}

    def test_create_problem(self):
        response = self.client.post(
            '/courses/1/problems',
            json={'description': 'Test problem'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('problem_id', data)

    def test_create_problem_wrong_course(self):
        response = self.client.post(
            '/courses/12/problems',
            json={'description': 'Test problem'}
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {'error': 'Курс не найден'})

    def test_get_problems(self):
        problems[1] = {"problem_id": 1, "course_id": 1, "description": "Test problem"}
        response = self.client.get('/courses/1/problems')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)

    def test_update_problem(self):
        problems[1] = {"problem_id": 1, "course_id": 1, "description": "Old description"}
        response = self.client.patch(
            '/courses/1/problems/1',
            json={'description': 'New description'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "Задача обновлена успешно"})

    def test_delete_problem(self):
        problems[1] = {"problem_id": 1, "course_id": 1, "description": "Test problem"}
        response = self.client.delete('/courses/1/problems/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "Задача удалена успешно"})

    def test_solve_problem(self):
        problems[1] = {"problem_id": 1, "course_id": 1, "description": "Test problem"}
        response = self.client.put(
            '/courses/1/problems/1/solve',
            json={'solution': 'Test solution', 'student_id': 1}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "Задача решена успешно"})

    def test_grade_problem(self):
        problems[1] = {"problem_id": 1, "course_id": 1, "description": "Test problem", "grades": {}}
        response = self.client.post(
            '/courses/1/problems/1/grade',
            json={'grade': 'A', 'student_id': 1}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, {"message": "Оценка задачи обновлена успешно"})

if __name__ == '__main__':
    unittest.main()
