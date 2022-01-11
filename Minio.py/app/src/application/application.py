from flask import json,jsonify,Blueprint
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from src.infrastructure.fsServices.fsService import FsService
from dotenv import load_dotenv
from src.interface.index import resources_dict 
import os
from ast import literal_eval
load_dotenv('.env', verbose=True)
from swagger.swagger import generated_swagger

SERVER_URL = os.getenv('SERVER_URL')
SWAGGER_URL = '/api/docs'
API_URL = '/app/swagger.json'
BUCKETS = literal_eval(os.getenv('BUCKETS'))

def Application(app,api_fs):
    # ======================== Initializing APP =======================
    @api_fs.route(API_URL, methods=['GET'])
    def swagger_api_docs_yml():
        try:
            generated_swagger['servers'] = [{'url':f'http://{SERVER_URL}:5002/api'}]
            return generated_swagger
        except:
            pass

    swaggerui_bluprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL
    )
    api = Api(app,prefix='/api')


    # ========================= Add Resources =========================

    for routs in resources_dict.keys():
        for resource in resources_dict[routs]:  
            api.add_resource(resource[0],resource[1])
    # ======================= Register Bluprint =======================

    app.register_blueprint(api_fs)
    app.register_blueprint(swaggerui_bluprint)


    # ======================= Create Buckets ==========================
    print('BUCKETS:',BUCKETS)
    fs_service = FsService()
    fs_service.createBuckets(BUCKETS)    
    
    return app
