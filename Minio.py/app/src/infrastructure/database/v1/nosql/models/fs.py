from src.infrastructure.database.v1.nosql.models.AbstractRepository import AbstractRepository


def Create_Fs_Schema(db):
    model = db.create_collection('fs', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'additionalProperties': False,
            'properties': {
                '_id': {
                    'bsonType': 'objectId',
                    'description': 'Id of Object'
                },
                'order': {
                    'bsonType': 'int',
                    'description': 'set a title for template'
                },
                'title': {
                    'bsonType': 'string',
                    'description': 'set a title for template'
                },
                'filename': {
                    'bsonType': 'string',
                    'description': 'set the order_value for template'
                },
                'bucket_name': {
                    'bsonType': 'string',
                    'description': 'recognizing the product type'
                },
                'is_active': {
                    'bsonType': 'bool',
                    'description': 'recognizing record is active or not'
                },
                'is_deleted': {
                    'bsonType': 'bool',
                    'description': 'recognizing record is deleted or not'
                },
                'created_at': {
                    'bsonType': 'date',
                    'description': 'date of create'
                },
                'update_at': {
                    'bsonType': 'date',
                    'description': 'date of last update'
                }
            }
        }
    })

class FsModel(AbstractRepository):
    def __init__(self, db):
        self.model = db.get_collection('fs')
        super().__init__(db,self.model)
