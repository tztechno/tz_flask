from datetime import datetime
from flask_pymongo import PyMongo

mongo = PyMongo()

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.utcnow()

    @staticmethod
    def from_dict(data):
        return Post(data['title'], data['content'])
