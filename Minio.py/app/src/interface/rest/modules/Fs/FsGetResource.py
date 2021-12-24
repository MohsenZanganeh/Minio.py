
from src.interface.rest.modules.baseResource import baseResource
from src.application.v1.fs.GetFileUseCase import GetFileUseCase 
from flask import send_file
from src.domain.v1.fs import FsValidatore
fs_schema = FsValidatore().FsDownloadSchema

class FsGetFileResource(baseResource):
    def __init__(self):
        super().__init__()

    def get(self,bucket_name,owner_id,file_name):
        # Validation
        fs_json = self.query
        if fs_json:
            fs_schema(fs_json)
        
        # UseCase
        file = GetFileUseCase().GetFile(**self.query)
        
        return send_file(file,mimetype='image/png')
    