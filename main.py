from flask import Flask, request, redirect, render_template, send_from_directory, url_for, flash
import os
import sqlite3
import socket
import json
import shutil
from mutagen import File as MutagenFile
from pymediainfo import MediaInfo
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"
DATABASE = 'PyMediaServer.db'

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# --- DB Helpers ---
def connectDB():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initDB():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            with open('createdb.sql', 'r') as f:
                conn.executescript(f.read())
        print("Database Initialized")
    else:
        print("Database Already Exists")

# --- Media Folder Helpers ---
def createMediaFolders(config_path="mediapaths.json"):
    with open(config_path, "r") as f:
        paths = json.load(f)
    base = paths.get("base", "")
    for media_type, subpath in paths.items():
        if media_type == "base":
            continue
        full_path = os.path.join(base, subpath)
        os.makedirs(full_path, exist_ok=True)
        print(f"Ensured folder exists: {full_path}")

def getMediaFolder(media_type, config_path="mediapaths.json"):
    with open(config_path, "r") as f:
        paths = json.load(f)
    base = paths.get("base", "")
    subfolder = paths.get(media_type, "")
    full_path = os.path.join(base, subfolder)
    os.makedirs(full_path, exist_ok=True)
    return full_path

# --- Metadata Extractor ---
def extract_metadata(filepath):
    audio = MutagenFile(filepath)
    if not audio or not audio.info:
        return None

    def get_tag(*keys):
        for key in keys:
            if key in audio:
                value = audio[key]
                if isinstance(value, list):
                    return value[0]
                elif hasattr(value, 'text'):
                    return value.text[0]
                return str(value)
        return None

    title = get_tag("TIT2", "title")
    artist = get_tag("TPE1", "artist")
    album = get_tag("TALB", "album")
    duration = audio.info.length

    return {
        "title": title,
        "artist": artist,
        "album": album,
        "duration": duration,
    }
def extract_video_metadata(filepath):
    media_info = MediaInfo.parse(filepath)
    metadata = {
        "title": None,
        "show": None,
        "season": None,
        "episode": None,
        "episode_id": None,
        "release_date": None,
        "album_artist": None,
        "genre": None,
        "year": None,
        "description": None,
        "long_description": None,
        "rating": None,
        "runtime": None,
        "cover_exists": False,
    }

    for track in media_info.tracks:
        if track.track_type == "General":
            metadata["title"] = track.title
            metadata["show"] = track.collection
            metadata["season"] = track.season
            metadata["episode"] = track.part
            metadata["episode_id"] = track.part_id
            metadata["release_date"] = track.recorded_date
            metadata["album_artist"] = track.album_performer
            metadata["genre"] = track.genre
            metadata["year"] = track.recorded_date[:4] if track.recorded_date else None
            metadata["description"] = track.description
            metadata["long_description"] = getattr(track, "long_description", None)
            metadata["rating"] = getattr(track, "content_rating", None)
            metadata["runtime"] = track.duration / 60000 if track.duration else None

        elif track.track_type == "Image":
            metadata["cover_exists"] = True

    return metadata

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html', ip=IPAddr)
@app.route("/music")
def music():
    conn = connectDB()


@app.route('/tvshows')
def tvshows():
    conn = connectDB()
    shows = conn.execute("SELECT * FROM tvshows").fetchall()
    
@app.route('/tvshows/upload', methods=['GET', 'POST'])
def upload_tv():
    if request.method == 'GET':
        return render_template('upload_tvshows.html')

    uploaded_file = request.files.get('tvfile')
    if not uploaded_file or uploaded_file.filename == '':
        flash("No file uploaded")
        return redirect(request.url)

    filename = uploaded_file.filename
    temp_path = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)
    uploaded_file.save(temp_path)

    metadata = extract_video_metadata(temp_path)
    if not metadata:
        flash("Invalid video file")
        return redirect(request.url)

    showname = metadata["show"] or "Unknown Show"
    title = metadata["title"] or os.path.splitext(filename)[0]
    season = metadata["season"] or 1
    episode = metadata["episode"] or 1
    duration = metadata["runtime"] or 0

    dest_folder = getMediaFolder("tvshows")
    show_folder = os.path.join(dest_folder,showname, f"Season {season}")
    os.makedirs(show_folder, exist_ok=True)
    full_file_path = os.path.join(show_folder, filename)
    shutil.move(temp_path, full_file_path)

    conn = connectDB()
    conn.execute('''
        INSERT INTO tvshows (showname, season, episode, filename,original_filename)
        VALUES ( ?, ?, ?, ?,?)''',
        ( showname, season, episode, full_file_path,filename))
    conn.commit()
    conn.close()
    print("ADDED")
    print(showname)
    print(season)
    flash("TV Show uploaded!")
    return redirect(url_for('tvshows'))

@app.route('/users')
def users():
    conn = connectDB()
    users = conn.execute("SELECT * FROM users").fetchall()
    return render_template("")
if __name__ == '__main__':
    initDB()
    createMediaFolders()
    app.run(host="0.0.0.0", port=7075, debug=True)
