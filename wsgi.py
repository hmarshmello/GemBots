import sys
import os

# Add the api directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api')))

from app import app

if __name__ == "__main__":
    app.run()
