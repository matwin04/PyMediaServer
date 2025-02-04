class Shows:
    def __init__(self,conn):
        self.conn = conn

    def addShows(self,show_name,season,episode,genre):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO shows (show_name,season,episode,genre) VALUES (?,?,?,?)",show_name,season,episode,genre)
        self.conn.cursor()
    def getShows(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT * FROM shows").fetchall()