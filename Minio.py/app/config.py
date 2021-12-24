import os

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
MONGO = {
    'host':'mongo',
    'port': 27017,
    'database':'fs',
    'username':'mohsen',
    'password':'123'
}

TOPICS = ['broker_fs']

TOPICS = {'fs':'fs'}