import os
import time
from PIL import Image
import google.generativeai as genai
from flask import current_app
from .errors import AIError

class AIHandler:
    """Handle Gemini AI operations"""
    
    def __init__(self):
        """Initialize AI handler"""
        api_key = os.getenv("GOOGLE_GENERATIVEAI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_GENERATIVEAI_API_KEY not found in environment")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.chat = None
        
    def generate_response(self, prompt: str) -> str:
        """Generate response for a single prompt"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise AIError(f"Failed to generate response: {str(e)}")
            
    def analyze_image(self, image_path: str, prompt: str = None) -> str:
        """Analyze image with optional prompt"""
        try:
            image = Image.open(image_path)
            prompt = prompt or "Tell me about this picture"
            response = self.model.generate_content([prompt, image])
            return response.text
        except Exception as e:
            raise AIError(f"Failed to analyze image: {str(e)}")
            
    def start_chat(self, history=None) -> None:
        """Start or resume a chat session"""
        try:
            formatted_history = []
            if history:
                for msg in history:
                    if msg["role"] == "user":
                        formatted_history.append({
                            "role": "user",
                            "parts": [msg["message"]]
                        })
                    else:
                        formatted_history.append({
                            "role": "model",
                            "parts": [msg["message"]]
                        })
            
            self.chat = self.model.start_chat(history=formatted_history)
        except Exception as e:
            raise AIError(f"Failed to start chat: {str(e)}")
            
    def send_message(self, message: str) -> str:
        """Send message in chat session"""
        if not self.chat:
            self.start_chat()
            
        try:
            response = self.chat.send_message(message)
            return response.text.strip()
        except Exception as e:
            raise AIError(f"Failed to send message: {str(e)}")
            
    def analyze_multiple_images(self, image_paths: list, prompt: str) -> str:
        """Analyze multiple images with prompt"""
        try:
            images = [Image.open(path) for path in image_paths]
            content = [prompt] + images
            response = self.model.generate_content(content)
            return response.text
        except Exception as e:
            raise AIError(f"Failed to analyze images: {str(e)}")
            
    def analyze_document(self, file_path: str, prompt: str = None) -> str:
        """Analyze document (PDF, etc.)"""
        try:
            with open(file_path, 'rb') as file:
                document = file.read()
            prompt = prompt or "Summary of the given document:"
            response = self.model.generate_content([prompt, {"mime_type": "application/pdf", "data": document}])
            return response.text
        except Exception as e:
            raise AIError(f"Failed to analyze document: {str(e)}")
            
    def analyze_audio(self, audio_path: str, prompt: str = None) -> str:
        """Analyze audio file"""
        try:
            with open(audio_path, 'rb') as file:
                audio = file.read()
            prompt = prompt or "Summarize the audio:"
            response = self.model.generate_content([prompt, {"mime_type": "audio/mpeg", "data": audio}])
            return response.text
        except Exception as e:
            raise AIError(f"Failed to analyze audio: {str(e)}")
            
    def analyze_video(self, video_path: str, prompt: str = None) -> str:
        """Analyze video file"""
        try:
            with open(video_path, 'rb') as file:
                video = file.read()
            prompt = prompt or "Describe the clip:"
            response = self.model.generate_content([prompt, {"mime_type": "video/mp4", "data": video}])
            return response.text
        except Exception as e:
            raise AIError(f"Failed to analyze video: {str(e)}")
            
    def get_chat_history(self) -> list:
        """Get current chat history"""
        if not self.chat:
            return []
            
        try:
            return [
                {
                    "role": "user" if msg["role"] == "user" else "bot",
                    "message": msg["parts"][0]
                }
                for msg in self.chat.history
            ]
        except Exception as e:
            return []
