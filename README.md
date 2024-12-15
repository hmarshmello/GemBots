# GemBots - AI Assistant Platform

A Flask-based web application that leverages Google's Gemini Pro AI model for various AI functionalities including text generation, image analysis, chat, and multimodal processing.

## Features

- 🤖 Interactive AI Chat
- 🖼️ Image Analysis
- 🎵 Audio Processing
- 🎥 Video Analysis
- 📄 PDF Document Processing
- 🌓 Dark/Light Theme
- 🔒 Secure File Handling
- 📊 Rate Limiting
- 🛡️ CSRF Protection

## Tech Stack

- Python 3.11
- Flask 3.0.0
- Google Generative AI (Gemini Pro)
- Pillow for image processing
- Modern CSS with dark mode support
- Secure file handling
- Comprehensive logging

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GemBots.git
cd GemBots
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Generate secret keys using:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

5. Run the application:
```bash
# Development mode
python wsgi.py

# Production mode (Linux/macOS)
gunicorn wsgi:app

# Production mode (Windows)
waitress-serve --port=8000 wsgi:app
```

## Project Structure

```
GemBots/
├── api/                    # Application package
├── public/                 # Static files
│   ├── css/               # Stylesheets
│   └── uploads/           # File uploads
├── templates/             # HTML templates
└── logs/                  # Application logs
```

See `structure_gembots.txt` for detailed project structure.

## Development

1. Enable debug mode:
```bash
# In .env file
FLASK_DEBUG=1
```

2. Monitor logs:
- `logs/info.log`: General information
- `logs/error.log`: Error tracking
- `logs/werkzeug.log`: Web server logs

3. Run tests:
```bash
python -m pytest
```

## Deployment

### Render.com (Recommended)

1. Push to GitHub
2. Create new Web Service in Render
3. Connect repository
4. Set environment variables:
   - FLASK_DEBUG=0
   - FLASK_SECRET_KEY
   - GOOGLE_GENERATIVEAI_API_KEY
   - CSRF_SECRET_KEY
5. Deploy

### Manual Deployment

1. Set production environment:
```bash
# In .env file
FLASK_DEBUG=0
```

2. Use production server:
```bash
# Linux/macOS
gunicorn wsgi:app

# Windows
waitress-serve --port=8000 wsgi:app
```

## Security Features

- CSRF Protection
- Rate Limiting
- Secure File Handling
- Session Security
- Error Handling
- Request Logging

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Generative AI
- Flask Framework
- Modern CSS Features
- Security Best Practices
