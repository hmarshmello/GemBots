import os
from typing import List, Tuple
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif'},
    'audio': {'mp3', 'wav', 'ogg'},
    'video': {'mp4', 'webm', 'avi'},
    'pdf': {'pdf'}
}

def allowed_file(filename: str, file_type: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, set())

def validate_file(file, file_type: str, max_size_mb: int = 100) -> Tuple[bool, str]:
    """Validate file type and size."""
    if not file:
        return False, "No file provided"
    
    if not allowed_file(file.filename, file_type):
        return False, f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS[file_type])}"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset file pointer
    
    if size > max_size_mb * 1024 * 1024:
        return False, f"File too large. Maximum size is {max_size_mb}MB"
    
    return True, "File is valid"

def save_file(file, upload_folder: str) -> Tuple[bool, str]:
    """Save file to upload folder."""
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return True, filename
    except Exception as e:
        return False, str(e)

def cleanup_old_files(folder: str, max_files: int = 100):
    """Delete old files if folder exceeds max_files."""
    try:
        files = os.listdir(folder)
        if len(files) > max_files:
            files.sort(key=lambda x: os.path.getctime(os.path.join(folder, x)))
            for file in files[:-max_files]:
                os.remove(os.path.join(folder, file))
    except Exception as e:
        print(f"Error cleaning up files: {e}")

def format_chat_history(history: List[dict]) -> List[dict]:
    """Format chat history for Gemini model."""
    formatted_history = []
    for msg in history:
        if msg["role"] == "user":
            formatted_history.append({"role": "user", "parts": [msg["message"]]})
        else:
            formatted_history.append({"role": "model", "parts": [msg["message"]]})
    return formatted_history
