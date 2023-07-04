from .__innit__ import API
from src.item.response import new_response
from src.item.database import Database
from src.app.PlaylistOperations import PlaylistOperations
from src.app.UserInfo import UserInfo


class DatabaseOperations:
    def __init__(self):
        self.api = API()
        self.user = UserInfo()
        
    def add_playlist_to_database(self, playlist_name, database_name):
        """
        Adds songs from a playlist to a database
        """
        x = PlaylistOperations()
        playlist_id = x.get_playlist_by_name(playlist_name).id
        if ".db" not in database_name:
            database_name = database_name
        db = Database(database_name)
        db.create_table()
        results = x.get_playlist_tracks(playlist_name)
        playlist_id = db.create_playlist(playlist_name)
       
        for track in results:
            song_name = track.name   
            artists = ', '.join(artist['name'] for artist in track.artists)
            album = track.album['name']
            db.store_song_in_playlist(playlist_id, song_name, artists, album)

    def get_all_playlists1(self,limit=50):
        json = {'limit': limit}
        request = new_response.get(f'/me/playlists', self.api.token, json=json)
        return request
    
    def get_all_playlists(self,limit=50, offset=0):
        """
        Returns the list of the playlists owned or followed by a Spotify user
        """
        params = {'limit': limit, 'offset': offset}
        total_playlists = PlaylistOperations().get_playlist_count()
        playlists = []
        while offset < total_playlists:
            request = new_response.get(f'/users/{self.user.user_id()}/playlists', self.api.token, params=params)
            playlists.extend(request['items'])
            offset += limit
        return playlists
            
    def create_backup_library(self):
        """
        Creates a backup database library containing every single playlist and every song in each playlist
        """
        users_playlists = self.get_all_playlists()
        user_playlist_id_list = [(item['id'], item['name'], item['tracks']['total']) for item in users_playlists]
        db = Database("backup_db.db")
        db.create_backup_library() 
        for item in user_playlist_id_list:
            tracks = PlaylistOperations().get_playlist_tracks(item[1])
            playlist_id = db.create_backup_playlist(item[1], item[0], item[2])
            for track in tracks:
                if track:
                    song_name = track.name
                    artist = track.artists[0]['name']
                    track_id = track.id    
                    db.store_song_in_backup_playlist(playlist_id, song_name, artist, track_id)       
        print('Finished creating the backup library')                                     

 