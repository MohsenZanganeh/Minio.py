from werkzeug.datastructures import FileStorage
from src.interface.rest.errors.ErrorHandler import BAD_REQUEST
from src.interface.rest.constants.statusCodes import SUCCESS
from src.infrastructure.fsServices.fsService import FsService
from utils.image_utils import convert_format_of_image,read_file, resize_image
from src.infrastructure.database.v1.nosql.db import db
import uuid

class PutFileUseCase():
    def __init__(self):
        self.fs = db().fs()
    def putFile(self,bucket_name,files,owner_id):
        fs_service = FsService()
        links = []
        for index,file in enumerate(files):
            content_type = file.content_type
            filename = file.filename
            extention = file.filename.split('.')[1]
            hashed_name = f'{uuid.uuid4()}.{extention}' 

            # is_exist = self.fs.get_one({'filename':filename})
            # if is_exist:
            #     raise BAD_REQUEST(f'this file {filename} is uploaded in advance')

            image = read_file(file)
            image = resize_image(image)
            image = convert_format_of_image(image,hashed_name)
            order = index+1
            self.fs.insert({
                'order':order,
                'filename':hashed_name,
                'title': filename,
                'bucket_name':bucket_name,
                'owner_id':owner_id
            })

            link = fs_service.putObject(bucket_name,image,f"{owner_id}/{hashed_name}",content_type)
            links.append({
                'filename':hashed_name,
                'title':filename,
                'order':order,
                'link':link
            })
        return SUCCESS(links)