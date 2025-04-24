from functools import wraps
from flask import request, jsonify
import base64


def basic_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"error": "Отсутствует заголовок авторизации"}), 401

        try:
            scheme, token = auth.split(" ", 1)
            if scheme.lower() != "basic":
                raise ValueError
            decoded = base64.b64decode(token).decode("utf-8")
            login, password = decoded.split(":", 1)
        except Exception:
            return jsonify({"error": "Неверный формат заголовка авторизации"}), 401

        # Проверка пользователя в базе данных
        from src.database import users
        user = next(
            (user for user in users.values() if user.get('login') == login and user.get('password') == password), None)
        if not user:
            return jsonify({"error": "Неверные учетные данные"}), 401

        # Сохранение авторизованного пользователя в запросе
        request.user = user

        return f(*args, **kwargs)

    return decorated_function
