from src.interface.rest.constants.statusCodes import SUCCESS
from src.infrastructure.fsServices.fsService import FsService
class GetFileUseCase(): 

    def GetFile(self,**query):
        fs_service = FsService()
        get_object = fs_service.getObject(query['bucket_name'],query['file_name'])
        return get_object