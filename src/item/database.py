import sqlite3
import os

class Database:
    def __init__(self, db_file):
        if not db_file.endswith('.db'):
            db_file += '.db'
            
        db_path = os.path.join('database', db_file)
        
        self.conn = sqlite3.connect(db_path)
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
################################ BACKUP PLAYLIST FUNCTIONS ################################
###########################################################################################
 
    def create_backup_library(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_playlists(
                playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_name TEXT,
                user_playlist_id TEXT,
                song_amount TEXT
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
    
    def create_backup_playlist(self, playlist_name, playlist_id, song_amount):
        self.cursor.execute('INSERT INTO backup_playlists (playlist_name, user_playlist_id, song_amount) VALUES (?, ?, ?)', (playlist_name, playlist_id, song_amount))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def store_song_in_backup_playlist(self, playlist_id, song_name, song_artist, track_id):
        self.cursor.execute('INSERT INTO backup_songs (playlist_id, song_name, song_artist, track_id) VALUES (?, ?, ?, ?)', (playlist_id, song_name, song_artist, track_id))
        self.conn.commit()
        

###########################################################################################
################################ PLAYLIST GENERATOR FUNCTIONS ################################
###########################################################################################
 

    def create_playlist_generator_library(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_playlists(
                playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                playlist_name TEXT,
                song_amount TEXT
            )
        ''')
        
        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS backup_songs(
               song_id INTEGER PRIMARY KEY,
               playlist_id INTEGER,
               song_name TEXT,
               song_artist TEXT,
               track_id TEXT,
               FOREIGN KEY (playlist_id) REFERENCES generated_playlists (playlist_id)
           )                 
        ''')
        
    def create_generated_playlist(self, playlist_name, song_amount):
        self.cursor.execute('INSERT INTO generated_playlists (playlist_name, song_amount) VALUES (?, ?)', ( playlist_name, song_amount))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def store_song_in_generated_playlist_library(self, playlist_id, song_name, song_artist, track_id):
        self.cursor.execute('INSERT INTO backup_songs (playlist_id, song_name, song_artist, track_id) VALUES (?, ?, ?, ?)', (playlist_id, song_name, song_artist, track_id))
        self.conn.commit()
        