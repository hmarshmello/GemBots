import os
import logging
from logging.handlers import RotatingFileHandler
from flask import request, has_request_context

class RequestFormatter(logging.Formatter):
    """Custom formatter that includes request info"""
    
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.path = request.path
        else:
            record.url = None
            record.remote_addr = None
            record.method = None
            record.path = None
            
        return super().format(record)

def init_logging(app):
    """Initialize logging configuration"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set basic logging config
    logging.basicConfig(level=logging.INFO)
    
    # Create formatters
    console_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s - %(method)s %(path)s %(levelname)s: %(message)s'
    )
    
    file_formatter = RequestFormatter(
        '%(asctime)s - %(remote_addr)s - %(method)s %(url)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Create file handlers
    info_file_handler = RotatingFileHandler(
        'logs/info.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(file_formatter)
    
    error_file_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(file_formatter)
    
    # Create werkzeug logger
    werkzeug_handler = RotatingFileHandler(
        'logs/werkzeug.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    werkzeug_handler.setLevel(logging.INFO)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addHandler(werkzeug_handler)
    
    # Add handlers to app logger
    app.logger.addHandler(console_handler)
    app.logger.addHandler(info_file_handler)
    app.logger.addHandler(error_file_handler)
    
    # Set app logger level
    app.logger.setLevel(logging.INFO)
    
    # Log startup
    app.logger.info('Application startup')
    
    # Request logging
    @app.before_request
    def log_request_info():
        app.logger.info('Request: %s %s', request.method, request.url)
        app.logger.debug('Headers: %s', dict(request.headers))
        app.logger.debug('Body: %s', request.get_data())
    
    # Response logging
    @app.after_request
    def log_response_info(response):
        app.logger.info(
            'Response: %s %s %s',
            request.method,
            request.url,
            response.status
        )
        return response
    
    # Error logging
    @app.errorhandler(Exception)
    def log_exception(error):
        app.logger.exception('Unhandled exception: %s', str(error))
        raise error
    
    return app
