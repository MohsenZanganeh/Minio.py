from datetime import datetime
from bson import json_util, ObjectId
import json
from pymongo.errors import WriteError,DuplicateKeyError
from src.interface.rest.errors.ErrorHandler import BAD_REQUEST


class AbstractRepository():
    relations = []

    def __init__(self,db, model,relations=[]):
        self.model = model
        self.db = db
        self.relations = relations

    def insert(self, data):
        data['is_deleted'] = False
        data['is_active'] = True
        data['created_at'] = datetime.now()
        try:
            model = self.model.insert_one(data)
            return str(model.inserted_id)

        except DuplicateKeyError as err:
            self._duplicate_error_handler(err)
        except WriteError as err:
            self._write_error_handler(err)

    def insert_many(self, data):
        for item in data:
            item['is_deleted'] = False
            item['is_active'] = True
            item['created_at'] = datetime.now()
        try:
            model = self.model.insert_many(data)
            return model
        except DuplicateKeyError as err:
            self._duplicate_error_handler(err)
        except WriteError as err:
            self._write_error_handler(err)
    def delete(self, id):
        return self.model.update_one({'_id': id},{'$set': {'is_deleted': True}})

    def updateById(self, id, data):
        data['update_at'] = datetime.now()
        try:
            self.model.update_one({'_id': id,'is_deleted':False}, {'$set': data})
            return str(id)
        except DuplicateKeyError as err:
            self._duplicate_error_handler(err)
        except WriteError as err:
            self._write_error_handler(err)

    def updateByQuery(self, kwargs, data):
        data['update_at'] = datetime.now()
        kwargs['is_deleted'] = False
        try:
            self.model.update_one(kwargs, {'$set': data})
            return self._parse_json(self.model.find_one(kwargs))
        except DuplicateKeyError as err:
            self._duplicate_error_handler(err)
        except WriteError as err:
            self._write_error_handler(err)
    def get_one(self, kwargs, join = False,select=None):
        data = self.model.find_one(kwargs,select)
        parsed_data = self._parse_json(data)
        
        if join:
            self.join(parsed_data,is_list = False)   

        return parsed_data

    def get_all(self,  join = False,select=None,**kwargs):
        data = self.model.find(kwargs,select)
        parsed_data = self._parse_json(data)

        if join:
            self.join(parsed_data,True)   

        return parsed_data

    def join(self,data, is_list = False):
        select = {'is_deleted':0,'created_at':0,'update_at':0,'is_active':0,'version':0}
        for relation in self.relations:
            field_name = relation['field']
            field_model = relation['model']
            if is_list:
                for object in data:
                    if object.get(field_name):
                        id = ''
                        if not isinstance(object[field_name],int):
                            id = ObjectId(object[field_name].get('$oid'))
                        else:
                            id = object[field_name]

                        model = self.db.get_collection(field_model)
                        found_object = model.find_one({'_id': id,'is_deleted':False},select)
                        object[field_name]  = self._parse_json(found_object)
            else:
                if data.get(field_name):
                    id = ''
                    if not isinstance(data[field_name],int):
                        id = ObjectId(data[field_name].get('$oid'))
                    else:
                        id = data[field_name]

                    model = self.db.get_collection(field_model)
                    found_object = model.find_one({'_id': id,'is_deleted':False},select)
                    data[field_name]  = self._parse_json(found_object)

    def _parse_json(self, data):
        return json.loads(json_util.dumps(data))

    def _write_error_handler(self,err):
        err =  self._parse_json(err.details)
        # err = json.loads(err)
        err = err['errInfo']['details']['schemaRulesNotSatisfied'][0]
        errorDeserialized = []
        if 'propertiesNotSatisfied' in err:
            err = err['propertiesNotSatisfied']  
            for property in err:
                errorDeserialized.append({
                    'propertyName': property['propertyName'],
                    'reason': property['details'][0]['reason'],
                    'consideredType': property['details'][0]
                    # 'consideredType': self._get_consider_type(property['details'][0])
                })
        else:
            errorDeserialized.append(err)
        
        raise BAD_REQUEST(errorDeserialized)
            
    def _duplicate_error_handler(self,err):
        First_index = (err._message.find('index') + 6)
        err = (err._message)[First_index:]
        Second_index = (err.find('dup key:') )
        err = (err)[:Second_index]


        
        raise BAD_REQUEST("Duplicate: " + err)