import os
import json
from flask import Flask, request
import yt_dlp
from google.cloud import storage

app = Flask(__name__)
storage_client = storage.Client()

@app.route("/", methods=["POST"])
def ingest_video():
    """
    Expects JSON: {"url": "...", "nikaya": "...", "book": "...", "start_x": "..."}
    """
    data = request.get_json()
    url = data.get("url")

    # Metadata for GCS
    metadata = {
        "nikaya": data.get("nikaya"),
        "book": data.get("book"),
        "start_x": data.get("start_x")
    }

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/video.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

        bucket = storage_client.bucket(os.environ.get("RAW_BUCKET"))
        blob = bucket.blob(f"raw_{info['id']}.mp3")
        blob.metadata = metadata
        blob.upload_from_filename(file_path)

    return {"status": "success", "file": blob.name}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
