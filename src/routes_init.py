from src.topics import init_topic_routes
from src.users import init_user_routes
from src.courses import init_course_routes
from src.problems import init_problem_routes
from src.registration import registration_route


def init_routes(app):
    init_user_routes(app)
    init_topic_routes(app)
    init_course_routes(app)
    init_problem_routes(app)
    registration_route(app)