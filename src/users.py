from flask import request, jsonify
from src.classes import User
from src.database import users


def init_user_routes(app):
    @app.route("/users", methods=["POST"])
    def create_user():
        global user_id_counter
        user_data = request.get_json()
        user = User(**user_data)
        users[user_id_counter] = user.__dict__
        user_id_counter += 1
        return jsonify(
            {"id": user_id_counter - 1,
             "message": "User created successfully"}
        )

    @app.route("/users/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        if user_id not in users:
            return jsonify({"error": "User not found"}), 404
        user_data = request.get_json()
        user = User(**user_data)
        users[user_id] = user.__dict__
        return jsonify({"message": "User updated successfully"})

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        if user_id not in users:
            return jsonify({"error": "User not found"}), 404
        del users[user_id]
        return jsonify({"message": "User deleted successfully"})
