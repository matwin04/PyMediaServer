import sqlite3
class Movies:
    def __init__(self,dbPath="media.db"):
        self.dbPath = dbPath
    def addMovie(self,title,year,genre):
        with sqlite3.connect(self.dbPath) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO movies(title,year,genre) VALUES(?,?,?)",(title,year,genre))
            conn.commit()

    def getMovies(self):
        with sqlite3.connect(self.dbPath) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM movies")
            return cursor.fetchall()