import datetime
import uuid

from database import Database
from models.post import Post


class Blog(object):

    def __init__(self, author, title, description, id=None):
        self.author = author
        self.title= title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id

    @classmethod
    def from_mongo(cls, id):
        data = Database.find_one(table='blogs', data={'id':id})
        return cls(author=data['author'],
                   title=data['title'],
                   description=data['description'],
                   id=id)

    def get_posts(self):
        return Post.from_blog(self.id)

    def new_post(self):
        title = input("Enter your post Title: ")
        comment = input("Enter the comment: ")
        date = input("Enter post date in format DDMMYYY or leave blank for today: ")
        if date == "":
            date = datetime.datetime.utcnow()
        else:
            date = datetime.datetime.strptime(date, "%d%m%Y")

        new_post = Post(blog_id= self.id,
                        title=title,
                        comment=comment,
                        author=self.author,
                        date= date)

        new_post.save_to_mongo()

    def save_to_mongo(self):
        Database.insert('blogs', self.json())

    def json(self):
        return {'author':self.author,
                'title': self.title,
                'description': self.description,
                'id': self.id}