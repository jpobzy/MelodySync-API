import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_id INTEGER,
                song_name TEXT,
                artist TEXT,
                album TEXT,
                FOREIGN KEY (playlist_id) REFERENCES playlists (playlist_id)
            )
        ''')

    def create_playlist(self, playlist_name):
        self.cursor.execute('INSERT INTO playlists (playlist_name) VALUES (?)', (playlist_name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def store_song_in_playlist(self, playlist_id, song_name, artist, album):
        self.cursor.execute('''
            INSERT INTO songs (playlist_id, song_name, artist, album)
            VALUES (?, ?, ?, ?)
        ''', (playlist_id, song_name, artist, album))
        self.conn.commit()

    def retrieve_playlist_songs(self, playlist_id):
        self.cursor.execute('SELECT * FROM songs WHERE playlist_id = ?', (playlist_id,))
        return self.cursor.fetchall()

