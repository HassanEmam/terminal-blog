from database import Database
from models.blog import Blog


class Menu (object):

    def __init__(self):
        self.user = input("Enter your username: ")
        self.user_blog = None
        if self._user_has_account():
            print("Welcome back {}".format(self.user))
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        blog = Database.find_one('blogs', {'author': self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else:
            return False

    def _prompt_user_for_account(self):
        title = input('Enter blog title: ')
        description = input('Enter description: ')
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        read_write = input('Do you want to (R)ead or (W)rite blogs? ')
        read_write = read_write.upper()

        if read_write == 'R':
            self._list_blogs()
            self._view_blog()

            pass

        elif read_write == 'W':
            self._prompt_write_post()

        else:
            print('Thank you for blogging!')

    def _list_blogs(self):
        blogs= Database.find(table='blogs',
                             data={})
        for blog in blogs:
            print("ID: {}, Author: {}, Title: {}".format(blog['id'], blog['author'], blog['title']))

    def _view_blog(self):
        blog_to_see = input("enter the id of the blog you want to read: ")
        blog = Blog.from_mongo(blog_to_see)
        posts = blog.get_posts()
        print(blog.id, blog.title)
        for post in posts:
            print("Date: {}, Title {} \n\n{}".format(post['date'], post['title'], post['comment']))

    def _prompt_write_post(self):
        self.user_blog.new_post()