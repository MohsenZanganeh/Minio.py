
from src.interface.rest.modules.baseResource import baseResource
from src.application.v1.fs.DeleteFileUseCase import DeleteFileUseCase 
from src.domain.v1.fs import FsValidatore
fs_schema = FsValidatore().FsDeleteSchema

class FsDeleteResource(baseResource):
    def __init__(self):
        super().__init__()

    def delete(self,bucket_name,file_name):
        # Validation
        fs_json = self.query
        if fs_json:
            fs_schema(fs_json)
        
        # UseCase
        return DeleteFileUseCase().deleteFile(**self.query)       
    