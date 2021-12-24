import json
from bson.objectid import ObjectId
from flask_restful import Resource
from flask import request

class baseResource(Resource):
    def __init__(self):
        data = request.get_json()
        self.props = {}
        if request.files:
            self.files = request.files.getlist('file')

        if request.form:
            form = {}
            for key in request.form.keys():
                try:
                    form[key] = json.loads(request.form.get(key))
                except:
                    form[key] = request.form.get(key)
            self.props = form

        if isinstance(data,dict):
            self.props = request.get_json()
            if self.props.get('user'):
                del self.props['user']
        self.query = {}
        if request.args:
            request.args = dict(request.args)
            print('=====request.args:',request.args)
            if request.args.get('id'):
               request.args['id'] = ObjectId(request.args['id'])

            elif request.args.get('_id'):
               request.args['id'] = ObjectId(request.args['_id'])
               del request.args['_id']

            self.query = {**request.args,**self.query}
        
        if request.view_args:
            if request.view_args.get('id'):
               request.view_args['id'] = ObjectId(request.view_args['id'])

            elif request.view_args.get('_id'):
               request.view_args['id'] = ObjectId(request.view_args['_id'])
               del request.view_args['_id']
             
             
                
            self.query = {**request.view_args,**self.query}