import unittest
from src.routes_init import init_routes
from flask import Flask
from src.database import users
from src.classes import User


class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        init_routes(self.app)
        self.client = self.app.test_client()
        users.clear()
        users[1] = User(1, "bobrik", "bober", "kurwik", "student", " 1234")

    def test_registration_student_success(self):
        """
        Тестирование успешной регистрации студента.
        """
        response = self.client.post(
            '/auth/signIn',
            json={
                'login': 'student1',
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'role': 'student'
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        # Проверяем, что ответ содержит ожидаемые поля
        self.assertIn('user_id', data)
        self.assertIn('login', data)
        self.assertIn('role', data)
        self.assertIn('password', data)  # Пароль должен быть сгенерирован

        # Проверяем, что пользователь добавлен в систему
        self.assertIn(data['user_id'], users)
        self.assertEqual(users[data['user_id']].login, 'student1')
        self.assertEqual(users[data['user_id']].role, 'student')

    def test_registration_teacher_success(self):
        """
        Тестирование успешной регистрации преподавателя.
        """
        response = self.client.post(
            '/auth/signIn',
            json={
                'login': 'teacher1',
                'first_name': 'Анна',
                'last_name': 'Петрова',
                'role': 'teacher',
                'password': 'teacher123'  # Пароль указан вручную
            }
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        # Проверяем, что ответ содержит ожидаемые поля
        self.assertIn('user_id', data)
        self.assertIn('login', data)
        self.assertIn('role', data)
        self.assertNotIn('password', data)  # Пароль не возвращается для роли 'teacher'

        # Проверяем, что пользователь добавлен в систему
        self.assertIn(data['user_id'], users)
        self.assertEqual(users[data['user_id']].login, 'teacher1')
        self.assertEqual(users[data['user_id']].role, 'teacher')

    def test_registration_missing_fields(self):
        """
        Тестирование регистрации с отсутствием обязательных полей.
        """
        response = self.client.post(
            '/auth/signIn',
            json={
                'login': 'user1',
                'first_name': 'Петр'
                # Пропущены last_name и role
            }
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_registration_duplicate_login(self):
        """
        Тестирование регистрации с дубликатом логина.
        """
        # Регистрируем первого пользователя
        self.client.post(
            '/auth/signIn',
            json={
                'login': 'user2',
                'first_name': 'Ольга',
                'last_name': 'Олеговна',
                'role': 'student'
            }
        )

        # Пытаемся зарегистрировать второго пользователя с тем же логином
        response = self.client.post(
            '/auth/signIn',
            json={
                'login': 'user2',
                'first_name': 'Ирина',
                'last_name': 'Иванова',
                'role': 'student'
            }
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_registration_invalid_role(self):
        """
        Тестирование регистрации с некорректной ролью.
        """
        response = self.client.post(
            '/auth/signIn',
            json={
                'login': 'user3',
                'first_name': 'Сергей',
                'last_name': 'Сергеев',
                'role': 'invalid_role'  # Некорректная роль
            }
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
