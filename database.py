import pymongo

class Database(object):

    URI ="mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE= client['fullstack']

    @staticmethod
    def insert(table, data):
        Database.DATABASE[table].insert(data)

    @staticmethod
    def find(table, data):
        return Database.DATABASE[table].find(data)

    @staticmethod
    def find_one(table, data):
        return Database.DATABASE[table].find_one(data)