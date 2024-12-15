import os
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    # Get the parent directory of the api folder
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', secrets.token_urlsafe(32))
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB limit
    
    # Static and template folders
    STATIC_FOLDER = os.path.join(BASE_DIR, "public")
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
    
    # Upload folders
    UPLOAD_FOLDER_IMAGE = os.path.join(BASE_DIR, "public/uploads/images")
    UPLOAD_FOLDER_AUDIO = os.path.join(BASE_DIR, "public/uploads/audio")
    UPLOAD_FOLDER_VIDEO = os.path.join(BASE_DIR, "public/uploads/video")
    UPLOAD_FOLDER_PDF = os.path.join(BASE_DIR, "public/uploads/pdf")
    
    # File limits
    MAX_FILES_PER_FOLDER = 1000
    MAX_FILE_SIZE_MB = 100
    
    # API settings
    GEMINI_API_KEY = os.getenv('GOOGLE_GENERATIVEAI_API_KEY')
    GEMINI_MODEL = "gemini-1.5-pro"

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment."""
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    env = 'development' if debug_mode else 'production'
    return config.get(env, config['default'])
