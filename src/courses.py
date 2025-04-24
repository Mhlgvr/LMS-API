from flask import request, jsonify
from src.classes import Course
from src.database import courses

course_id_counter = 1

def init_course_routes(app):
    @app.route("/courses", methods=["POST"])
    def create_course():
        global course_id_counter
        course_data = request.get_json()
        course = Course(course_id_counter, course_data['name'], course_data['description'])
        courses[course_id_counter] = course.__dict__
        course_id_counter += 1
        return jsonify(
            {"id": course_id_counter - 1,
             "message": "Course created successfully"}
        )

    @app.route("/courses/<int:course_id>", methods=["PUT"])
    def update_course(course_id):
        if course_id not in courses:
            return jsonify({"error": "Course not found"}), 404
        course_data = request.get_json()
        course = Course(**course_data)
        courses[course_id] = course.__dict__
        return jsonify({"message": "Course updated successfully"})

    @app.route("/courses/<int:course_id>", methods=["DELETE"])
    def delete_course(course_id):
        if course_id not in courses:
            return jsonify({"error": "Course not found"}), 404
        del courses[course_id]
        return jsonify({"message": "Course deleted successfully"})
