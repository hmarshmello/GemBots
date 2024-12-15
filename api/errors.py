from flask import jsonify, render_template, request
from werkzeug.http import HTTP_STATUS_CODES

class APIError(Exception):
    """Base API Exception"""
    status_code = 500

    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status_code
        rv['error'] = HTTP_STATUS_CODES.get(self.status_code, 'Unknown error')
        return rv

class ValidationError(APIError):
    """Validation error"""
    def __init__(self, message):
        super().__init__(message, status_code=400)

class FileError(APIError):
    """File handling error"""
    def __init__(self, message):
        super().__init__(message, status_code=400)

class AIError(APIError):
    """AI processing error"""
    def __init__(self, message):
        super().__init__(message, status_code=500)

def register_error_handlers(app):
    """Register error handlers with the Flask app"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        if request_wants_json():
            return jsonify({'error': 'Not found', 'status': 404}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request_wants_json():
            return jsonify({'error': 'Internal server error', 'status': 500}), 500
        return render_template('errors/500.html'), 500

    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        if request_wants_json():
            return response
        return render_template('errors/error.html', 
                             error=error.message, 
                             status=error.status_code), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return handle_api_error(error)

    @app.errorhandler(FileError)
    def handle_file_error(error):
        return handle_api_error(error)

    @app.errorhandler(AIError)
    def handle_ai_error(error):
        return handle_api_error(error)

def request_wants_json():
    """Check if the request wants a JSON response"""
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']
