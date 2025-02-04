class Movies:
    def __init__(self, conn):
        self.conn = conn

    def addMovie(self, title, year, genre):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO movies (title, year, genre) VALUES (?, ?, ?)", (title, year, genre))
        self.conn.commit()

    def getMovies(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT * FROM movies").fetchall()
