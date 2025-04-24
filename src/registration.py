from flask import request, jsonify
import uuid
from src.database import users
from src.classes import User


def registration_route(app):
    @app.route('/auth/signIn', methods=["POST"])
    def registration():
        data = request.get_json() or {}

        required_fields = ['login', 'first_name', 'last_name', 'role']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Отсутствуют обязательные поля"}), 400

        login = data['login']
        first_name = data['first_name']
        last_name = data['last_name']
        role = data['role'].lower()

        if any(user.login == login for user in users.values()):
            return jsonify({"error": "Логин уже занят"}), 400

        password = data.get("password") or (str(uuid.uuid4()) if role == "student" else None)

        if role not in ['student', 'teacher']:
            return jsonify({"error": "Некорректная роль"}), 400

        user_id = len(users) + 1
        users[user_id] = User(
            user_id, login, first_name, last_name, role, password
        )

        response = {
            "message": "Пользователь зарегистрирован",
            "user_id": user_id,
            "login": login,
            "role": role
        }
        if role == "student":
            response["password"] = password

        return jsonify(response), 201
