import sqlite3

class Database:
    def __init__(self, db_file):
        if not db_file.endswith('.db'):
            db_file += '.db'
        
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


 ###########################################################################################
 
    def create_backup_library(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_playlists(
                playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_name TEXT,
                user_playlist_id TEXT  
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_songs(
                song_id INTEGER PRIMARY KEY,
                playlist_id INTEGER,
                song_name TEXT,
                song_artist TEXT,
                track_id TEXT,
                FOREIGN KEY (playlist_id) REFERENCES backup_playlists (playlist_id)
            )                    
        ''')
    
    def create_backup_playlist(self, playlist_name, playlist_id):
        self.cursor.execute('INSERT INTO backup_playlists (playlist_name, user_playlist_id) VALUES (?, ?)', (playlist_name, playlist_id))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def store_song_in_backup_playlist(self, playlist_id, song_name, song_artist, track_id):
        self.cursor.execute('INSERT INTO backup_songs (playlist_id, song_name, song_artist, track_id) VALUES (?, ?, ?, ?)', (playlist_id, song_name, song_artist, track_id))
        self.conn.commit()
        