import os
import sys

# Get the absolute path of the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))

# Add the project directory to Python path
sys.path.insert(0, project_dir)

# Import the Flask application
from api.app import app

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run the app
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.getenv("FLASK_ENV") == "development"
    )
