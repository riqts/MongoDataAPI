import config
from mongo_client import MongoDBClient


def get_mongodb():
    return MongoDBClient.get_instance().get_database()