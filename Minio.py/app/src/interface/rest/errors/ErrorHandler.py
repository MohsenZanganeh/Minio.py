class NOT_FOUND(Exception):
        code = 404
        description = 'NOT FOUND'

class BAD_REQUEST(Exception):
        code = 500
        description = 'BAD_REQUEST'

class VALIDATION_ERROR(Exception):
        code = 400
        description = 'VALIDATION_ERROR'
        
class INVALID_CREDENTIALS(Exception):
        code = 401
        description = 'INVALID_CREDENTIALS'