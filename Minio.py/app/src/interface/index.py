from src.interface.rest.modules.Fs import FsDownloadResource,FsDeleteResource,FsPutResource,FsGetResource
resources_dict = {
    'fs':[
        [FsDownloadResource.FsDownloadResource ,'/fs/<string:file_name>/<string:bucket_name>'],
        [FsDeleteResource.FsDeleteResource ,'/fs/<string:file_name>/<string:bucket_name>'],
        [FsGetResource.FsGetFileResource ,'/fs/download/<string:file_name>/<string:bucket_name>'],
        [FsPutResource.FsPutResource ,'/fs/<string:bucket_name>']
    ],
}
