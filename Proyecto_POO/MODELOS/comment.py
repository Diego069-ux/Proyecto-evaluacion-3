# models.py

class Post:
    def __init__(self, title, body, userId, id=None):
        self.id = id
        self.title = title
        self.body = body
        self.userId = userId

    def __repr__(self):
        return f"<Post {self.id} - {self.title}>"