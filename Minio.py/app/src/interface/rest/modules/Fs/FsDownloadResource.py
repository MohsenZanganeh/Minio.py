
from src.interface.rest.modules.baseResource import baseResource
from src.application.v1.fs.DownloadLinkUseCase import DownloadLinkUseCase 
from src.domain.v1.fs import FsValidatore
fs_schema = FsValidatore().FsDownloadSchema

class FsDownloadResource(baseResource):
    def __init__(self):
        super().__init__()

    def get(self,bucket_name,file_name):
        # Validation
        fs_json = self.query
        if fs_json:
            fs_schema(fs_json)
        
        # UseCase
        file = DownloadLinkUseCase().downloadLink(**self.query)
        return file
    