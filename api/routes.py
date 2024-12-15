from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
    g,
    send_from_directory,
    jsonify
)
import os
from .errors import ValidationError, FileError, AIError
from .ai_handler import AIHandler
from .file_handler import FileHandler

def init_app(app):
    """Initialize routes with the Flask app"""
    
    @app.before_request
    def before_request():
        """Set up request context"""
        g.ai_handler = AIHandler()
        g.file_handlers = {
            'image': FileHandler('image'),
            'audio': FileHandler('audio'),
            'video': FileHandler('video'),
            'pdf': FileHandler('pdf')
        }
    
    # Theme toggle endpoint
    @app.route('/toggle-theme', methods=['POST'])
    def toggle_theme():
        try:
            data = request.get_json()
            theme = data.get('theme')
            
            if theme not in ['light', 'dark']:
                return jsonify({'error': 'Invalid theme'}), 400
                
            session['theme'] = theme
            return jsonify({'status': 'success', 'theme': theme})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # Serve static files
    @app.route('/public/<path:filename>')
    def serve_static(filename):
        return send_from_directory(app.static_folder, filename)
    
    @app.route("/")
    def index():
        return render_template("index.html", theme=session.get('theme', 'light'))

    @app.route("/single_prompt", methods=["GET", "POST"])
    def single_prompt():
        if request.method == "POST":
            user_input = request.form.get("prompt")
            if not user_input:
                raise ValidationError("Please provide a prompt")
            
            try:
                generated_text = g.ai_handler.generate_response(user_input)
                return render_template(
                    "single_prompt.html",
                    generated_text=generated_text,
                    prompt=user_input,
                )
            except Exception as e:
                flash(str(e))
                return render_template("single_prompt.html")
                
        return render_template("single_prompt.html")

    @app.route("/image_text", methods=["GET", "POST"])
    def image_text():
        if request.method == "POST":
            if "image" not in request.files:
                raise ValidationError("No file provided")
                
            file = request.files["image"]
            if not file.filename:
                raise ValidationError("No file selected")
                
            try:
                filename = g.file_handlers['image'].save_file(file)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER_IMAGE'], filename)
                
                generated_text = g.ai_handler.analyze_image(image_path)
                
                return render_template(
                    "image_text.html",
                    generated_text=generated_text,
                    image_url=url_for("static", filename=f"uploads/images/{filename}"),
                )
            except Exception as e:
                flash(str(e))
                return render_template("image_text.html")
                
        return render_template("image_text.html")

    @app.route("/interactive_chat", methods=["GET", "POST"])
    def interactive_chat():
        if "chat_history" not in session:
            session["chat_history"] = []
            try:
                g.ai_handler.start_chat()
                response = g.ai_handler.send_message(
                    "You are a helpful AI assistant. Please introduce yourself briefly."
                )
                session["chat_history"] = [{"role": "bot", "message": response}]
            except Exception as e:
                flash(str(e))
                return render_template(
                    "interactive_chat.html",
                    chat_history=[]
                )

        if request.method == "POST":
            user_message = request.form.get("message")
            if not user_message:
                raise ValidationError("Please provide a message")
                
            try:
                g.ai_handler.start_chat(session["chat_history"])
                bot_message = g.ai_handler.send_message(user_message)
                
                session["chat_history"].append(
                    {"role": "user", "message": user_message}
                )
                session["chat_history"].append(
                    {"role": "bot", "message": bot_message}
                )
                session.modified = True
                
            except Exception as e:
                flash(str(e))

        return render_template(
            "interactive_chat.html",
            chat_history=session.get("chat_history", [])
        )

    @app.route("/reset_chat")
    def reset_chat():
        session.pop("chat_history", None)
        return redirect(url_for("interactive_chat"))

    @app.route("/multi_image_prompt", methods=["GET", "POST"])
    def multi_image_prompt():
        if request.method == "POST":
            user_input = request.form.get("prompt")
            if not user_input:
                raise ValidationError("Please provide a prompt")
                
            images = request.files.getlist("images")
            if len(images) < 2:
                raise ValidationError("Please upload at least two images")
                
            try:
                image_paths = []
                image_urls = []
                
                for img in images:
                    filename = g.file_handlers['image'].save_file(img)
                    image_paths.append(os.path.join(current_app.config['UPLOAD_FOLDER_IMAGE'], filename))
                    image_urls.append(
                        url_for("static", filename=f"uploads/images/{filename}")
                    )
                
                generated_text = g.ai_handler.analyze_multiple_images(
                    image_paths, user_input
                )
                
                return render_template(
                    "multi_image_prompt.html",
                    generated_text=generated_text,
                    image_urls=image_urls,
                    prompt=user_input,
                )
            except Exception as e:
                flash(str(e))
                return render_template("multi_image_prompt.html")
                
        return render_template("multi_image_prompt.html")

    @app.route("/multimodal_audio", methods=["GET", "POST"])
    def multimodal_audio():
        if request.method == "POST":
            if "audio" not in request.files:
                raise ValidationError("No file provided")
                
            file = request.files["audio"]
            if not file.filename:
                raise ValidationError("No file selected")
                
            try:
                filename = g.file_handlers['audio'].save_file(file)
                audio_path = os.path.join(current_app.config['UPLOAD_FOLDER_AUDIO'], filename)
                
                generated_text = g.ai_handler.analyze_audio(audio_path)
                
                return render_template(
                    "multimodal_audio.html",
                    generated_text=generated_text,
                    audio_url=url_for("static", filename=f"uploads/audio/{filename}"),
                )
            except Exception as e:
                flash(str(e))
                return render_template("multimodal_audio.html")
                
        return render_template("multimodal_audio.html")

    @app.route("/multimodal_video_prompt", methods=["GET", "POST"])
    def multimodal_video_prompt():
        if request.method == "POST":
            if "video" not in request.files:
                raise ValidationError("No file provided")
                
            file = request.files["video"]
            if not file.filename:
                raise ValidationError("No file selected")
                
            try:
                filename = g.file_handlers['video'].save_file(file)
                video_path = os.path.join(current_app.config['UPLOAD_FOLDER_VIDEO'], filename)
                
                generated_text = g.ai_handler.analyze_video(video_path)
                
                return render_template(
                    "multimodal_video_prompt.html",
                    generated_text=generated_text,
                    video_url=url_for("static", filename=f"uploads/video/{filename}"),
                )
            except Exception as e:
                flash(str(e))
                return render_template("multimodal_video_prompt.html")
                
        return render_template("multimodal_video_prompt.html")

    @app.route("/pdf_prompt", methods=["GET", "POST"])
    def pdf_prompt():
        if request.method == "POST":
            if "pdf" not in request.files:
                raise ValidationError("No file provided")
                
            file = request.files["pdf"]
            if not file.filename:
                raise ValidationError("No file selected")
                
            try:
                filename = g.file_handlers['pdf'].save_file(file)
                pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER_PDF'], filename)
                
                generated_text = g.ai_handler.analyze_document(pdf_path)
                
                return render_template(
                    "pdf_prompt.html",
                    generated_text=generated_text,
                    pdf_url=url_for("static", filename=f"uploads/pdf/{filename}"),
                )
            except Exception as e:
                flash(str(e))
                return render_template("pdf_prompt.html")
                
        return render_template("pdf_prompt.html")
