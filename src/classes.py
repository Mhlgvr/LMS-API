class User:
    def __init__(self, user_id, login, first_name, last_name, role, password):
        self.user_id = user_id
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.password = password

    def update(self, login=None, first_name=None, last_name=None, role=None, password=None):
        if login:
            self.login = login
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if role:
            self.role = role
        if password:
            self.password = password


class Course:
    def __init__(self, course_id, name, description):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.topics = []

    def add_topic(self, topic):
        self.topics.append(topic)

    def update(self, name=None, description=None):
        if name:
            self.name = name
        if description:
            self.description = description


class Topic:
    def __init__(self, topic_id, title, content):
        self.topic_id = topic_id
        self.title = title
        self.content = content

    def update(self, title=None, content=None):
        if title:
            self.title = title
        if content:
            self.content = content

    def to_dict(self):
        return {
            "topic_id": self.topic_id,
            "title": self.title,
            "content": self.content
        }


class Problem:
    def __init__(self, problem_id, course_id, description, solution=None):
        self.problem_id = problem_id
        self.course_id = course_id
        self.description = description
        self.solution = solution
        self.grades = {}

    def solve(self, student_id, solution):
        self.solution = solution
        self.grades[student_id] = "Pending"

    def grade(self, student_id, grade):
        if student_id in self.grades:
            self.grades[student_id] = grade
