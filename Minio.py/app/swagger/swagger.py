import os
from dotenv import load_dotenv
load_dotenv('.env', verbose=True)
SERVER_URL = os.getenv('SERVER_URL')

swagger = {
    "openapi": "3.0.0",
    "info": {
        "version": "1.0.0",
        "title": "FS",
        "contact": "null",
        "description": "Apis"
        f'''
       <a href="http://{SERVER_URL}:5002/api/docs">Fs Service</a>
       '''
    },
    "paths": {
        "/fs/{bucket_name}": {
            "put": {
                "tags": [
                    "Fs"
                ],
                "summary": "Put Your File Do this with Postman",
                "consumes": [
                    "multipart/form-data"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [
                    {
                        "in": "path",
                        "name": "bucket_name",
                        "type": "string",
                        "description": "bucket_name of file"
                    }
                ],
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "file": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "format": "binary"
                                        }
                                    }
                                }
                            },
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Created"
                    }
                }
            }
        },
        "/fs/download/{file_name}/{bucket_name}": {
            "get": {
                "tags": [
                    "Fs"
                ],
                "summary": "get File",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "multipart/form-data"
                ],
                "parameters": [
                    {
                        "in": "path",
                        "name": "file_name",
                        "description": "file_name for get the file",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "in": "path",
                        "name": "bucket_name",
                        "description": "bucket_name for get the file",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "get file"
                    }
                }
            }
        },
        "/fs/{file_name}/{bucket_name}": {
            "get": {
                "tags": [
                    "Fs"
                ],
                "summary": "get File",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "multipart/form-data"
                ],
                "parameters": [
                    {
                        "in": "path",
                        "name": "file_name",
                        "description": "file_name for get the file",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "in": "path",
                        "name": "bucket_name",
                        "description": "bucket_name for get the file",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "get file"
                    }
                }
            },

            "delete": {
                "tags": [
                    "Fs"
                ],
                "summary": "Delete Your File Do this with Postman",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [
                    {
                        "in": "path",
                        "name": "file_name",
                        "description": "file_name for get the file",
                        "schema": {
                            "type": "string"
                        }
                    },
                    {
                        "in": "path",
                        "name": "bucket_name",
                        "description": "bucket_name for get the file",
                        "schema": {
                            "type": "string"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "delete file"
                    }
                }
            }
        }
    }
}


def generate_swagger(swagger):
    for path in swagger['paths']:
        methods = swagger['paths'][path]
        for method in methods:
            is_public = methods[method].get('is_public')
            if is_public == None or is_public == False:
                methods[method]['security'] = [{'bearerAuth': []}]
    return swagger


generated_swagger = generate_swagger(swagger)
