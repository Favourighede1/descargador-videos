from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        formato = request.form["formato"]
        filename = "video." + ("mp4" if formato in ["mp4", "4k"] else formato)
        ydl_opts = {
            "outtmpl": filename,
            "format": "bestvideo+bestaudio/best" if formato == "4k" else "bestaudio/best",
            "postprocessors": []
        }

        if formato in ["mp3", "wav"]:
            ydl_opts["format"] = "bestaudio"
            ydl_opts["postprocessors"].append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": formato,
                "preferredquality": "192",
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filename, as_attachment=True)

    return render_template("index.html")
