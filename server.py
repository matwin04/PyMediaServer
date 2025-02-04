from flask import *
import sqlite3

app = Flask(__name__)
def initDB():
    dbPath = "media.db"
    sqlFiles = ["sql/movies.sql", "sql/tvshows.sql", "sql/music.sql", "sql/videos.sql"]

    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        for sqlFile in sqlFiles:
            with open(sqlFile, "r") as file:
                cursor.executescript(file.read())
        conn.commit()
@app.route("/")
def index():
    return render_template("index.html")