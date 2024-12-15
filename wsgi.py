import os
from api import create_app

# Create Flask application with environment-specific config
# Use FLASK_DEBUG for development mode instead of deprecated FLASK_ENV
debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
environment = "development" if debug_mode else "production"

app = create_app(environment)

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))

    # Run the app
    app.run(
        host="0.0.0.0",  # Required for Render.com
        port=port,
        debug=debug_mode,
    )
