from minio import Minio, InvalidResponseError
import os

from src.interface.rest.errors.ErrorHandler import NOT_FOUND
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
MINIO_ACCESS_KEY = os.getenv('MINIO_ROOT_USER')
MINIO_SECRET_KEY = os.getenv('MINIO_ROOT_PASSWORD')
SERVER_URL = os.getenv('SERVER_URL')

class FsService():
    def __init__(self):
        self.client = Minio(
            f'{SERVER_URL}:9000',
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )

    def createBuckets(self, buckets_name):
        for bucket_name in buckets_name:
            if(not self.client.bucket_exists(bucket_name)):
                self.client.make_bucket(bucket_name)

    def putObject(self, bucket_name, file,filename,content_type): 
        self.client.put_object(
            bucket_name=bucket_name,
            object_name=filename,
            data=file,
            length=-1,
            content_type=content_type,
            part_size=5*1024*1024
        )
        return self.downloadLinkObject(bucket_name,filename)

    def removeObject(self, bucket_name, file_name):
        try:
            self.client.remove_object(bucket_name, file_name)
        except InvalidResponseError as identifier:
            raise identifier

    def getObject(self, bucket_name, file_name):
        try:
            response = self.client.get_object(bucket_name, f'{file_name}')
            return response
            # Read data from response.
        except:
            raise NOT_FOUND('your file not found')
        
    def downloadLinkObject(self, bucket_name, file_name):
        return self.client.presigned_get_object(bucket_name,file_name)