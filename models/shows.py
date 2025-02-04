class Shows:
    def __init__(self,conn):
        self.conn = conn

    def addShows(self,show_name,season,episode,episodeName,sourceFormat,genre):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO shows (show_name,season,episode,episodeName,sourceFormat,genre) VALUES (?,?,?,?,?,?)",show_name,season,episode,episodeName,sourceFormat,genre)
        self.conn.cursor()
    def getShows(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT * FROM shows").fetchall()