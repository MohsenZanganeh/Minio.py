from marshmallow import Schema, fields, validate
from marshmallow.exceptions import ValidationError
from src.interface.rest.errors.ErrorHandler import BAD_REQUEST
from werkzeug.datastructures import FileStorage
import os
from ast import literal_eval
BUCKETS = literal_eval(os.getenv('BUCKETS'))
from src.domain.v1.validatore import validatore

class FsValidatore():

    def FsDownloadSchema(self, data):
        return validatore(data, {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "enum": BUCKETS
                    },
                    "owner_id": {
                        "type": "string"
                    },
                    "file_name": {
                        "type": "string"
                    }
                },
                "required": ["bucket_name","file_name"],
                "additionalProperties": False
            }
        })

    def FsPutSchema(self, data):
        return validatore(data, {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "enum": BUCKETS
                    },
                    "owner_id": {
                        "type": "string"
                    }
                },
                "required": ["bucket_name"],
                "additionalProperties": False
            }
        })
        
    def FsDeleteSchema(self, data):
        return validatore(data, {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "enum": BUCKETS
                    },
                    "owner_id": {
                        "type": "string"
                    },
                    "file_name": {
                        "type": "string"
                    }
                },
                "required": ["bucket_name","file_name"],
                "additionalProperties": False
            }
        })
    def FsFileSchema(self,files):
        if files is [] or files is None:
            BAD_REQUEST('No file part')
        if not isinstance(files,list):
            ValidationError('your file must be in a array object')
        
        for file in files:
            if file.filename == '':
                ValidationError("one of your files hasn't name")
        return files


