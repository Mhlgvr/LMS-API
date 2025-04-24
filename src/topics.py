from flask import request, jsonify
from src.classes import Topic
from src.database import courses, topics


def init_topic_routes(app):
    @app.route('/courses/<int:course_id>/topics', methods=['POST'])
    def create_topic(course_id):
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Нет данных'}), 400

        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        new_topic_id = len(topics)+1
        new_topic = Topic(new_topic_id, data['title'], data['content'])
        topics[new_topic_id] = new_topic
        courses[course_id].add_topic(new_topic)
        return jsonify(new_topic.to_dict()), 201

    @app.route('/courses/<int:course_id>/topics/<int:topic_id>',
               methods=['PUT', 'PATCH'])
    def update_topic(course_id, topic_id):
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Нет данных'}), 400

        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        if topic_id not in topics.keys():
            return jsonify({'error': 'Тема не найдена'}), 404
        topic = topics[topic_id]
        topic.update(data['title'], data['content'])
        return jsonify(topic.to_dict()), 200

    @app.route('/courses/<int:course_id>/topics/<int:topic_id>',
               methods=['DELETE'])
    def delete_topic(course_id, topic_id):
        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404
        elif topic_id not in topics.keys():
            return jsonify({'error': 'Тема не найдена'}), 404
        del topics[topic_id]
        return jsonify({'message': 'Тема удалена успешно'}), 200
