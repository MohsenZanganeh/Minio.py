from src.infrastructure.database.v1.nosql.models import fs
import config
from pymongo import MongoClient


class db():

    def __init__(self):
        self.client = MongoClient(
            config.MONGO['host'],
            config.MONGO['port'],
            username=config.MONGO['username'],
            password=config.MONGO['password'])[config.MONGO['database']]


    def fs(self):
        if ('fs' in self.client.list_collection_names()) == False:
            fs.Create_Fs_Schema(self.client)
        return fs.FsModel(self.client)