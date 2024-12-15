import os
from werkzeug.utils import secure_filename
from flask import current_app
from .errors import FileError

class FileHandler:
    """Handle file operations"""
    
    ALLOWED_EXTENSIONS = {
        'image': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
        'audio': {'mp3', 'wav', 'ogg', 'm4a'},
        'video': {'mp4', 'webm', 'avi', 'mov'},
        'pdf': {'pdf'}
    }
    
    def __init__(self, file_type):
        """Initialize file handler with file type"""
        self.file_type = file_type
        self.upload_folder = None
        
    def _get_upload_folder(self):
        """Get upload folder path based on file type"""
        folder_map = {
            'image': current_app.config['UPLOAD_FOLDER_IMAGE'],
            'audio': current_app.config['UPLOAD_FOLDER_AUDIO'],
            'video': current_app.config['UPLOAD_FOLDER_VIDEO'],
            'pdf': current_app.config['UPLOAD_FOLDER_PDF']
        }
        
        folder = folder_map.get(self.file_type)
        if folder:
            os.makedirs(folder, exist_ok=True)
        return folder
        
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS[self.file_type]
            
    def save_file(self, file):
        """Save file with basic validation"""
        if not file:
            raise FileError("No file provided")
            
        filename = secure_filename(file.filename)
        if not filename:
            raise FileError("Invalid filename")
            
        if not self.allowed_file(filename):
            raise FileError(
                f"Invalid file type. Allowed types: {', '.join(self.ALLOWED_EXTENSIONS[self.file_type])}"
            )
            
        # Get upload folder within application context
        if not self.upload_folder:
            self.upload_folder = self._get_upload_folder()
            
        # Generate unique filename
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(self.upload_folder, filename)):
            filename = f"{base}_{counter}{ext}"
            counter += 1
            
        file_path = os.path.join(self.upload_folder, filename)
        file.save(file_path)
        
        return filename
        
    def cleanup_old_files(self, max_files=1000):
        """Delete old files if folder exceeds max_files"""
        try:
            if not self.upload_folder:
                self.upload_folder = self._get_upload_folder()
                
            files = os.listdir(self.upload_folder)
            if len(files) > max_files:
                files.sort(key=lambda x: os.path.getctime(
                    os.path.join(self.upload_folder, x)
                ))
                for file in files[:-max_files]:
                    os.remove(os.path.join(self.upload_folder, file))
        except Exception as e:
            print(f"Error cleaning up files: {str(e)}")
            
    def get_file_info(self, file_path):
        """Get file information"""
        try:
            size = os.path.getsize(file_path)
            created = os.path.getctime(file_path)
            modified = os.path.getmtime(file_path)
            
            return {
                'size': size,
                'created': created,
                'modified': modified
            }
        except Exception as e:
            print(f"Error getting file info: {str(e)}")
            return None
