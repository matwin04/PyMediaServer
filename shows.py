from flask import render_template
from main import app, connectDB


@app.route("/tvshows")
def tvshows():
    conn = connectDB()
    shows = conn.execute("SELECT * FROM tvshows")
    conn.close()
    return render_template("tvshows.html",tvshows=shows)
@app.route('/tvshows/upload',methods=["GET"])
def uploadMusicGet():
    return render_template('upload_shows.html')
