import os
import shutil
from flask import render_template, request, flash, redirect
from main import app, connectDB, IPAddr, getMediaFolder
from threading import Thread
from dave import start_dav_server

@app.route('/music')
def music():
    conn = connectDB()
    rows = conn.execute("SELECT * FROM music").fetchall()
    conn.close()
    return render_template('music.html', rows=rows, ip=IPAddr,title="Music")


@app.route('/music/upload',methods=["GET"])
def uploadMusicGet():
    return render_template('upload_music.html')


@app.route('/music/upload',methods=["POST"])
def uploadMusicPost():
    uploadedFile = request.files.get('musicfile')
    if not uploadedFile or uploadedFile.filename == '':
        flash("NO FILE UPLOADED")
        return redirect(request.url)
    filename = uploadedFile.filename
    tempPath = os.path.join("temp",filename)
    os.makedirs("temp",exist_ok=True)
    uploadedFile.save(tempPath)

    metadata = extract_metadata(tempPath)
    if not metadata:
        flash("Unsupported or unreadable file")
        return redirect(request.url)

    title = metadata["title"] or os.path.splitext(filename)[0]
    artist = metadata["artist"] or "Unknown Artist"
    album = metadata["album"] or "Unknown Album"


    destFolder = getMediaFolder("music")
    finalPath = os.path.join(destFolder,artist,album)
    os.makedirs(finalPath,exist_ok=True)
    full_file_path = os.path.join(finalPath, filename)
    shutil.move(tempPath, full_file_path)

    conn = connectDB()
    conn.execute('''
        INSERT INTO music (title, artist, album, filename)
        VALUES (?, ?, ?, ?)''',(title, artist, album, filename))
    conn.commit()
    conn.close()
    print("DONE")
    return redirect("/")
