from flask import Flask, g
from .config import get_config
from .errors import register_error_handlers
from .ai_handler import AIHandler
from .file_handler import FileHandler

def create_app(config_name='default'):
    """Application factory function"""
    
    # Create Flask app
    app = Flask(__name__,
                static_folder='../public',
                template_folder='../templates')
    
    # Load configuration
    app.config.from_object(get_config())
    
    # Initialize error handlers
    register_error_handlers(app)
    
    # Create upload directories
    with app.app_context():
        # Create file handlers to initialize directories
        file_handlers = {
            'image': FileHandler('image'),
            'audio': FileHandler('audio'),
            'video': FileHandler('video'),
            'pdf': FileHandler('pdf')
        }
        
        # Create upload directories
        for handler in file_handlers.values():
            handler._get_upload_folder()
    
    # Register routes
    from . import routes
    routes.init_app(app)
    
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app
