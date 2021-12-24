from src.interface.rest.constants.statusCodes import SUCCESS
from src.infrastructure.fsServices.fsService import FsService

class DeleteFileUseCase(): 

    def deleteFile(self,**query): 
        fs_service = FsService()
        fs_service.removeObject(query['bucket_name'],query['file_name'])
        return SUCCESS('Image was deleted Successfully')