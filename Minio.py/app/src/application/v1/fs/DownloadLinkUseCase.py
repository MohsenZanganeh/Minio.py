from src.interface.rest.constants.statusCodes import SUCCESS
from src.infrastructure.fsServices.fsService import FsService
class DownloadLinkUseCase(): 

    def downloadLink(self,**query):
        fs_service = FsService()
        downloadLink = fs_service.downloadLinkObject(query['bucket_name'],f"{query['owner_id']}/{query['file_name']}")

        return downloadLink