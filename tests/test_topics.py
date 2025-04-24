import unittest
from src.routes_init import init_routes
from flask import Flask
from src.database import courses, topics
from src.classes import Topic, Course


class TestTopics(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        init_routes(self.app)
        self.client = self.app.test_client()
        courses.clear()
        topics.clear()
        courses[1] = Course(1, "Изучение танков", "Играем в танки")
        topics[1] = Topic(1, "Практика танкования", "На ИС-4")

    def test_create_topic(self):
        response = self.client.post(
            '/courses/1/topics',
            json={'title': 'Изучения литрбола', 'content': 'Побольше пива!'}
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Изучения литрбола')
        self.assertEqual(data['content'], 'Побольше пива!')

    def test_create_wrong_topic(self):
        response = self.client.post(
            '/courses/1/topics',
            json={'content': 'Побольше пива'}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(
            data, {'error': 'Нет данных'}
        )

    def test_create_topic_wrong_course(self):
        response = self.client.post(
            '/courses/12/topics',
            json={'title': 'Изучения литрбола', 'content': 'Побольше пива'}
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(
            data, {'error': 'Курс не найден'}
        )

    def test_update_topic(self):
        response = self.client.put(
            '/courses/1/topics/1',
            json={'title': 'Изучения литрбола',
                  'content': 'Побольше пива и медовухи!'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Изучения литрбола')
        self.assertEqual(data['content'], 'Побольше пива и медовухи!')

    def test_update_wrong_topic(self):
        response = self.client.put(
            '/courses/1/topics/1',
            json={'title': 'Изучения литрбола'}
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(
            data, {'error': 'Нет данных'}
        )

    def test_update_topic_wrong_course(self):
        response = self.client.put(
            '/courses/12/topics/12',
            json={'title': 'Изучения литрбола', 'content': 'Побольше пива'}
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(
            data, {'error': 'Курс не найден'}
        )

    def test_delete_topic(self):
        response = self.client.delete(
            '/courses/1/topics/1'
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_wrong_topic(self):
        response = self.client.delete(
            '/courses/1/topics/12'
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(
            data, {'error': 'Тема не найдена'}
        )

    def test_delete_topic_wrong_course(self):
        response = self.client.delete(
            '/courses/12/topics/12'
        )
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(
            data, {'error': 'Курс не найден'}
        )


if __name__ == '__main__':
    unittest.main()
