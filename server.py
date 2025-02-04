from flask import *
import sqlite3
from models.movies import Movies
from models.shows import Shows
app = Flask(__name__)
def getDB():
    conn = sqlite3.connect("media.db")
    conn.row_factory =sqlite3.Row
    return conn
def initDB():
    dbPath = "media.db"
    sqlFiles = ["sql/movies.sql", "sql/shows.sql", "sql/music.sql", "sql/videos.sql"]

    with sqlite3.connect(dbPath) as conn:
        cursor = conn.cursor()
        for sqlFile in sqlFiles:
            with open(sqlFile, "r") as file:
                cursor.executescript(file.read())
        conn.commit()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/movies")
def movies():
    conn = getDB()
    movies = Movies(conn).getMovies()
    conn.close()
    return render_template("movies.html",movies=movies)
@app.route("/shows")
def shows():
    conn = getDB()
    shows = Shows(conn).getShows()
    conn.close()
    return render_template("shows.html",shows=shows)
