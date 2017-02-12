import datetime
import uuid

from database import Database


class Post:
    def __init__(self, blog_id, title, comment, author, date=datetime.datetime.utcnow(), id=None):
        self.blog_id = blog_id
        self.title = title
        self.author = author
        self.comment = comment
        self.id = uuid.uuid4().hex if id is None else id
        self.date_created=date

    def save_to_mongo(self):
        Database.insert('posts', self.json())

    def json(self):
        return {
            'id': self.id,
            'blog_id': self.blog_id,
            'author': self.author,
            'title': self.title,
            'comment': self.comment,
            'date': self.date_created
        }

    @classmethod
    def from_mongo(cls, id):
        data = Database.find_one(table='posts', data={'id': id})
        return cls(blog_id=data['blog_id'],
                   title=data['title'],
                   comment=data['comment'],
                   author=data['author'],
                   date=data['date'])

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(table='posts', data={'blog_id': id})]