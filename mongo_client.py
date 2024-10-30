from motor.motor_asyncio import AsyncIOMotorClient

import config


class MongoDBClient:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBClient._instance is None:
            MongoDBClient()
        return MongoDBClient._instance

    def __init__(self):
        if MongoDBClient._instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            MongoDBClient._instance = self
            self.client = AsyncIOMotorClient(config.MONGODB_URI, uuidRepresentation='standard')

    def get_database(self):
        if config.TEST == "1":
            self.client = AsyncIOMotorClient(config.MONGODB_URI, uuidRepresentation='standard')
            return self.client['test_hub']
        else:
            return self.client['hub']

    def close(self):
        self.client.close()