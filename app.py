from flask import Flask, request, render_template, send_file
import os
import yt_dlp as youtube_dl

app = Flask(__name__)

# Ensure the 'downloads' folder exists
os.makedirs("downloads", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        try:
            ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'ffmpeg_location': 'C:\\ffmpeg\\bin',  # 👈 This is the correct way (folder path only)
}

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)