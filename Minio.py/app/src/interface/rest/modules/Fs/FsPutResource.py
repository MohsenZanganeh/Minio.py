
from src.application.v1.fs.PutFileUseCase import PutFileUseCase
from src.interface.rest.modules.baseResource import baseResource
from flask import request   

from src.domain.v1.fs import FsValidatore
fs_schema = FsValidatore().FsPutSchema
fs_file_schema = FsValidatore().FsFileSchema


class FsPutResource(baseResource):
    def __init__(self):
        super().__init__()

    def put(self,bucket_name):
        # Validation
        fs_json = {**self.props,**self.query}
        if fs_json:
            fs_json = fs_schema(fs_json)

        files = fs_file_schema(self.files)
        # UseCase
        return PutFileUseCase().putFile(self.query['bucket_name'],
                                      files=files,
                                      owner_id=fs_json['owner_id'])
