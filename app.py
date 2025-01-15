from flask import Flask, request, render_template, send_file, jsonify
import os
from utils.process_video import process_video
from utils.LLM import process_prompt

# Initialize Flask app
app = Flask(__name__)

# Configure upload and output directories
UPLOAD_FOLDER = "video"
OUTPUT_FOLDER = "output"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Global variable to store processed video path
processed_video_path = None


@app.route("/", methods=["GET", "POST"])
def index():
    global processed_video_path

    if request.method == "POST":
        # Get form inputs
        video_url = request.form.get("video_url")
        uploaded_file = request.files.get("file")
        target_language = request.form.get("target_language")

        video_path = None

        # Handle video URL or uploaded file
        if video_url:
            video_path = video_url
        elif uploaded_file and uploaded_file.filename != "":
            video_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(video_path)
        else:
            return render_template("index.html", error="Please provide a video file or URL.")

        try:
            # Process the video using the provided path
            process_video(video_path, target_language=target_language)
            processed_video_path = "video_with_subtitles.mp4"

            return render_template(
                "result.html",
                video_output_path=processed_video_path,
            )
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

chat_history = []

@app.route("/chat", methods=["GET", "POST"])
def chat():
    global chat_history

    if request.method == "POST":
        user_input = request.form.get("user_input")  # Get the user's input

        if not user_input:
            return render_template("chat.html", chat_history=chat_history, error="Please enter a prompt.")

        try:
            # Call your process_prompt function to generate the response
            response = process_prompt(user_input)

            # Append the user's message and the LLM's response to the chat history
            chat_history.append({"type": "user", "message": user_input})
            chat_history.append({"type": "llm", "message": response})

            return render_template("chat.html", chat_history=chat_history)
        except Exception as e:
            return render_template("chat.html", chat_history=chat_history, error=str(e))

    return render_template("chat.html", chat_history=chat_history)


@app.route("/result", methods=["GET"])
def result():
    global processed_video_path

    if processed_video_path and os.path.exists(os.path.join(app.config["OUTPUT_FOLDER"], processed_video_path)):
        return render_template("result.html", video_output_path=processed_video_path)
    else:
        return render_template("result.html", error="No processed video found.")


@app.route("/download/<path:filename>")
def download(filename):
    file_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route("/cleanup/<path:filename>", methods=["DELETE"])
def cleanup(filename):
    file_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": "File deleted successfully"}), 200
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
