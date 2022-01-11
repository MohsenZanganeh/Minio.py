from marshmallow import ValidationError
from ma import ma  
from flask import Flask, jsonify,Blueprint

from src.interface.rest.errors.ErrorHandler import BAD_REQUEST, INVALID_CREDENTIALS,NOT_FOUND,VALIDATION_ERROR
from src.application.application import Application

# ================ Setup Application ================

app = Flask(__name__)
api_fs = Blueprint('api_fs', __name__)
app.config.from_object('config')
app =  Application(app,api_fs) 


# ======================= Error Handler =======================

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

@app.errorhandler(VALIDATION_ERROR)
@app.errorhandler(BAD_REQUEST)
@app.errorhandler(INVALID_CREDENTIALS)
@app.errorhandler(NOT_FOUND)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    description = 'Error'
    if hasattr(err,'description'):
       description = err.description
    
    code = 500
    if hasattr(err,'code'):
       code = err.code

    response = {"error": description}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors
    app.logger.error(f'{description}: {response["message"]}')
    return jsonify(response), code
    
if __name__ == '__main__':
    ma.init_app(app)
    app.run(port=5000, host='0.0.0.0')

