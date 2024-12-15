import os
import sys

# Add the api directory to Python path
sys.path.append(os.path.join(os.getcwd(), 'api'))

# Gunicorn config
bind = "0.0.0.0:" + os.getenv("PORT", "8000")
workers = 2
threads = 4
timeout = 120
accesslog = "-"
errorlog = "-"
capture_output = True
enable_stdio_inheritance = True
