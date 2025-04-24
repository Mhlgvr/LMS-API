from flask import request, jsonify
from src.classes import Problem
from src.database import problems, courses

def init_problem_routes(app):
    @app.route('/courses/<int:course_id>/problems', methods=['POST'])
    def create_problem(course_id):
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({'error': 'Нет данных'}), 400

        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        new_problem_id = len(problems)+1
        new_problem = Problem(new_problem_id, course_id, data['description'])
        problems[new_problem_id] = new_problem.__dict__
        return jsonify({"problem_id": new_problem_id, "message": "Задача создана успешно"}), 201

    @app.route('/courses/<int:course_id>/problems', methods=['GET'])
    def get_problems(course_id):
        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        course_problems = [problem for problem in problems.values() if problem['course_id'] == course_id]
        return jsonify(course_problems), 200

    @app.route('/courses/<int:course_id>/problems/<int:problem_id>', methods=['PATCH'])
    def update_problem(course_id, problem_id):
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({'error': 'Нет данных'}), 400

        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        if problem_id not in problems.keys():
            return jsonify({'error': 'Задача не найдена'}), 404

        problem = Problem(problem_id, course_id, data['description'])
        problems[problem_id] = problem.__dict__
        return jsonify({"message": "Задача обновлена успешно"}), 200

    @app.route('/courses/<int:course_id>/problems/<int:problem_id>', methods=['DELETE'])
    def delete_problem(course_id, problem_id):
        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        if problem_id not in problems.keys():
            return jsonify({'error': 'Задача не найдена'}), 404

        del problems[problem_id]
        return jsonify({"message": "Задача удалена успешно"}), 200

    @app.route('/courses/<int:course_id>/problems/<int:problem_id>/solve', methods=['PUT'])
    def solve_problem(course_id, problem_id):
        data = request.get_json()
        if not data or 'solution' not in data or 'student_id' not in data:
            return jsonify({'error': 'Нет данных'}), 400

        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        if problem_id not in problems.keys():
            return jsonify({'error': 'Задача не найдена'}), 404

        problem = Problem(problem_id, course_id, problems[problem_id]['description'])
        problem.solve(data['student_id'], data['solution'])
        problems[problem_id] = problem.__dict__
        return jsonify({"message": "Задача решена успешно"}), 200

    @app.route('/courses/<int:course_id>/problems/<int:problem_id>/grade', methods=['POST', 'PUT'])
    def grade_problem(course_id, problem_id):
        data = request.get_json()
        if not data or 'grade' not in data or 'student_id' not in data:
            return jsonify({'error': 'Нет данных'}), 400

        if course_id not in courses.keys():
            return jsonify({'error': 'Курс не найден'}), 404

        if problem_id not in problems.keys():
            return jsonify({'error': 'Задача не найдена'}), 404

        problem = Problem(problem_id, course_id, problems[problem_id]['description'])
        problem.grade(data['student_id'], data['grade'])
        problems[problem_id] = problem.__dict__
        return jsonify({"message": "Оценка задачи обновлена успешно"}), 200
