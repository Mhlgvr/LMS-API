from src.routes_init import init_routes
from flask import Flask
from flask import request, jsonify
from functools import wraps
from src.auth import basic_auth_required

app = Flask(__name__)
init_routes(app)

# Централизованная обработка исключений
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Страница не найдена"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500

# Контроль прав доступа
def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.user and request.user.role in role:
                return f(*args, **kwargs)
            else:
                return jsonify({"error": "Недостаточно прав"}), 403
        return decorated_function
    return decorator

@app.route("/test", methods=["GET"])
@basic_auth_required
def test():
    return "Success"

if __name__ == "__main__":
    app.run(debug=True)
