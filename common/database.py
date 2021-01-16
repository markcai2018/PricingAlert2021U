import pymongo
import os

class Database(object):
    
    #DB_USER = os.environ.get('DB_USER')
    URI = "mongodb+srv://root2511:mCai251101@cluster0-bpyjs.mongodb.net/student?retryWrites=true&w=majority"
    #URI = "mongodb+srv://" + DB_USER + "@cluster0-bpyjs.mongodb.net/student?retryWrites=true&w=majority"
    print(URI)
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['pricing']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)
