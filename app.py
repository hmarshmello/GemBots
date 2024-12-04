import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from flask_session import Session
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import secrets

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_urlsafe(32))

# Configure upload folders
app.config["UPLOAD_FOLDER_IMAGE"] = "static/uploads/images"
app.config["UPLOAD_FOLDER_AUDIO"] = "static/uploads/audio"
app.config["UPLOAD_FOLDER_VIDEO"] = "static/uploads/video"
app.config["UPLOAD_FOLDER_PDF"] = "static/uploads/pdf"
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB limit

# Ensure upload directories exist
os.makedirs(app.config["UPLOAD_FOLDER_IMAGE"], exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER_AUDIO"], exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER_VIDEO"], exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER_PDF"], exist_ok=True)

# Configure Google Generative AI
api_key = os.getenv("GOOGLE_GENERATIVEAI_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Please set GOOGLE_GENERATIVEAI_API_KEY in .env"
    )

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/single_prompt", methods=["GET", "POST"])
def single_prompt():
    if request.method == "POST":
        user_input = request.form.get("prompt")
        if user_input:
            try:
                response = model.generate_content([user_input])
                generated_text = "".join(chunk.text for chunk in response)
                return render_template(
                    "single_prompt.html",
                    generated_text=generated_text,
                    prompt=user_input,
                )
            except Exception as e:
                flash(f"Error: {str(e)}")
    return render_template("single_prompt.html")


@app.route("/image_text", methods=["GET", "POST"])
def image_text():
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER_IMAGE"], filename)
            file.save(image_path)
            try:
                organ = Image.open(image_path)
                response = model.generate_content(
                    ["Tell me about this instrument", organ]
                )
                generated_text = response.text
                return render_template(
                    "image_text.html",
                    generated_text=generated_text,
                    image_url=url_for("static", filename=f"uploads/images/{filename}"),
                )
            except Exception as e:
                flash(f"Error: {str(e)}")
    return render_template("image_text.html")


@app.route("/interactive_chat", methods=["GET", "POST"])
def interactive_chat():
    session["chat_history"] = [
        {"role": "user", "message": "Hello"},
        {
            "role": "bot",
            "message": "Great to meet you. What would you like to know? Please type 'OK,QUIT' to end the chat.",
        },
    ]
    if request.method == "GET":
        # Reset chat history on page load (including refresh
        x = 0
    elif request.method == "POST":
        # Handle user message submission
        user_message = request.form.get("message")
        if user_message:
            try:
                # Build chat prompt from history

                chat = model.start_chat(
                    history=[
                        {"role": "user", "parts": "Hello"},
                        {
                            "role": "model",
                            "parts": "Great to meet you. What would you like to know? "
                            "IF MENTIONED ANYTHING RELATED TO ENDING THE CHAT THEN RESPONDED WITH 'OK,QUIT' ONLY",
                        },
                    ]
                )
                # Generate response using google.generativeai's generate_chat method
                response = chat.send_message(user_message)
                bot_message = response.text.strip()

                # Append user and bot messages to chat history
                session["chat_history"].append(
                    {"role": "user", "message": user_message}
                )
                session["chat_history"].append({"role": "bot", "message": bot_message})

                # Check for termination condition
                if bot_message.upper() == "OK,QUIT":
                    session.pop("chat_history", None)

            except Exception as e:
                flash(f"Error: {str(e)}")

    return render_template(
        "interactive_chat.html", chat_history=session.get("chat_history", [])
    )


@app.route("/multi_image_prompt", methods=["GET", "POST"])
def multi_image_prompt():
    if request.method == "POST":
        user_input = request.form.get("prompt")
        images = request.files.getlist("images")
        if not user_input:
            flash("Please provide a prompt.")
            return redirect(request.url)
        if len(images) < 2:
            flash("Please upload at least two images.")
            return redirect(request.url)
        saved_images = []
        try:
            for img in images:
                if img and img.filename != "":
                    filename = secure_filename(img.filename)
                    img_path = os.path.join(app.config["UPLOAD_FOLDER_IMAGE"], filename)
                    img.save(img_path)
                    saved_images.append(Image.open(img_path))
            response = model.generate_content([user_input] + saved_images)
            generated_text = response.text
            image_urls = [
                url_for(
                    "static", filename=f"uploads/images/{secure_filename(img.filename)}"
                )
                for img in images
            ]
            return render_template(
                "multi_image_prompt.html",
                generated_text=generated_text,
                image_urls=image_urls,
                prompt=user_input,
            )
        except Exception as e:
            flash(f"Error: {str(e)}")
    return render_template("multi_image_prompt.html")


@app.route("/multimodal_audio", methods=["GET", "POST"])
def multimodal_audio():
    if request.method == "POST":
        if "audio" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["audio"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            audio_path = os.path.join(app.config["UPLOAD_FOLDER_AUDIO"], filename)
            file.save(audio_path)
            try:
                sample = genai.upload_file(audio_path)
                response = model.generate_content(["Summarize the audio", sample])
                generated_text = response.text
                return render_template(
                    "multimodal_audio.html",
                    generated_text=generated_text,
                    audio_url=url_for("static", filename=f"uploads/audio/{filename}"),
                )
            except Exception as e:
                flash(f"Error: {str(e)}")
    return render_template("multimodal_audio.html")


@app.route("/multimodal_video_prompt", methods=["GET", "POST"])
def multimodal_video_prompt():
    if request.method == "POST":
        if "video" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["video"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            video_path = os.path.join(app.config["UPLOAD_FOLDER_VIDEO"], filename)
            file.save(video_path)
            try:
                myfile = genai.upload_file(video_path)
                while myfile.state.name == "PROCESSING":
                    print("processing video...")
                    time.sleep(5)
                    myfile = genai.get_file(myfile.name)
                response = model.generate_content([myfile, "Describe the clip"])
                generated_text = response.text
                return render_template(
                    "multimodal_video_prompt.html",
                    generated_text=generated_text,
                    video_url=url_for("static", filename=f"uploads/video/{filename}"),
                )
            except Exception as e:
                flash(f"Error: {str(e)}")
    return render_template("multimodal_video_prompt.html")


@app.route("/pdf_prompt", methods=["GET", "POST"])
def pdf_prompt():
    if request.method == "POST":
        if "pdf" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["pdf"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER_PDF"], filename)
            file.save(pdf_path)
            try:
                sample_pdf = genai.upload_file(pdf_path)
                response = model.generate_content(
                    ["Summary of the given document:", sample_pdf]
                )
                generated_text = response.text
                return render_template(
                    "pdf_prompt.html",
                    generated_text=generated_text,
                    pdf_url=url_for("static", filename=f"uploads/pdf/{filename}"),
                )
            except Exception as e:
                flash(f"Error: {str(e)}")
    return render_template("pdf_prompt.html")


if __name__ == "__main__":
    app.run(debug=True)
