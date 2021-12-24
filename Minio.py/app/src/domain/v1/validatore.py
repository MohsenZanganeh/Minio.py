from src.interface.rest.errors.ErrorHandler import VALIDATION_ERROR
from jsonschema import Draft7Validator, exceptions, validators
from bson import ObjectId


def validatore(data, schema):
    
    validator = Draft7Validator(schema)
    errors = validator.iter_errors([data])
    deserialize_errors = []

    properties = schema['items']['properties']
    if data:
        for property in properties:
            if data.get(property):
                validated_object = objectId_validatore(properties[property],data[property],property)
                if isinstance(validated_object,dict):
                    if validated_object.get('error'):
                        deserialize_errors.append(validated_object['error'])

                if isinstance(validated_object,ObjectId):
                    del data[property] 
                    data[property] = validated_object
    else:
        raise VALIDATION_ERROR({'key':"none field", 'error':"you didn't sent any field"})
    if data.get('_id'):
        del data['_id']
    for error in sorted(errors, key=exceptions.relevance):
        deserialize_errors.append(
            {'key': error.path[-1], 'error': error.message})
    
    if deserialize_errors:
        raise VALIDATION_ERROR(deserialize_errors)
    return data





def objectId_validatore(object=None,data=None,property=None):
    error = None
    if not isinstance(object,str) and object.get('properties'):
        for obj_name in object.get('properties'):
            temp = data.get(obj_name)
            items_of_properties = object['properties'][obj_name]
            error = objectId_validatore(items_of_properties,
            temp,
            property=obj_name)

            if error:
                return error

    if not isinstance(object,str) and object.get('patternProperties'):
        properties_of_schema = object['patternProperties']['']
        if properties_of_schema.get('properties'):
            for each_key in data:
                for attribute in properties_of_schema:
                    if isinstance(properties_of_schema[attribute],dict):
                       if isinstance(data[each_key],dict):
                            for key in data[each_key]:
                                error = objectId_validatore(properties_of_schema['properties'][key], data[each_key][key],key)
                                
                                if isinstance(error,dict):
                                    if error.get('error'):
                                        return error


                       if properties_of_schema[attribute].get('type_id'):
                            id = data[each_key][attribute]
                            try:
                                id = ObjectId(id)
                                del data[each_key][attribute]
                                data[each_key][attribute] = id
                            except:
                                return {'error':{'key': property, 'error': "one of the object hasn't a valid field"},'status': False}



    if not isinstance(object,str) and object.get('items'):
        for attributes in object['items']:
            object_of_attributes = object['items'][attributes]
            if attributes == 'properties':
                for attribute_of_object_of_array in object_of_attributes:
                    for each_data in data:
                        each_data[attribute_of_object_of_array] = objectId_validatore(object_of_attributes[attribute_of_object_of_array],
                        each_data[attribute_of_object_of_array],
                        property=attribute_of_object_of_array)
            

            if object_of_attributes == "objectId":
                for id in data:
                   try:
                       ObjectId(id)
                   except: 
                      return {'error':{'key': property, 'error': 'Not a valid type'},'status': False}
                   index = data.index(id)
                   data[index] = ObjectId(id)

    if object.get('type_id'):
            try:
                return ObjectId(data)
            except: 
                return {'error':{'key': property, 'error': 'Not a valid type'},'status': False}

                
    return data