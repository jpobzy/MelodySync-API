from src.app.UserInfo import UserInfo
from src.item.response import new_response
from src.item.playlist import Playlist
from src.item.track import Track
from src.app.UserInfo import UserInfo
import random, qrcode

class PlaylistOperations:
    def __init__(self, api):
        self.api = api
        self.id = UserInfo(api).user_id
    
    def get_playlist_by_name(self, playlist_name, limit=50):
        """
        Returns a playlist object
        """
        self.api.token_expired()
        if any(playlist_name):
            params = {
                'limit': limit
            }
            get_users_playlists = new_response.get('/me/playlists', self.api.token, params)
            for i in get_users_playlists['items']:
                if i['name'].lower() == playlist_name.lower():
                    return Playlist(i)
        raise ValueError(f"Playlist with name '{playlist_name}' not found.")
      
    def update_playlist_name(self, old_playlist_name, new_playlist_name):
        """
        Updates a user's playlist name
        """   
        if any([old_playlist_name, new_playlist_name]):
            playlist_id = self.get_playlist_by_name(old_playlist_name).id
            json ={
                'name': new_playlist_name,
            }   
            new_response.put(f'/playlists/{playlist_id}', self.api.token, json=json) 
      
    def update_playlist_description(self, playlist_name, new_playlsit_description):
        """
        Updates a user's playlist name
        """   
        if any([playlist_name, new_playlsit_description]):
            playlist_id = self.get_playlist_by_name(playlist_name).id
            json ={
                'description': new_playlsit_description,
            }   
            new_response.put(f'/playlists/{playlist_id}', self.api.token, json=json)  
      
    def update_playlist_visibility(self, playlist_name, visibility_status):
        """Updates Playlist visibility

        Args:
            playlist_name (string): playlist name in library
            visibility_status (bool): True = Private, False == Public
        """
        if any([playlist_name, visibility_status]) and visibility_status == True or visibility_status == False:
            playlist_id = self.get_playlist_by_name(playlist_name).id
            json ={
                'public': visibility_status,
            }   
            new_response.put(f'/playlists/{playlist_id}', self.api.token, json=json)   
              
    def update_playlist_collaborative(self, playlist_name, collaborative_status):
        """Update the playlist to be collaborative or not, Note: You can only set collaborative to true on non-public playlists

        Args:
            playlist_name (string): playlist name in library
            collaborative_status (bool): True = collaborative, False == non collaborative
        """
        if any([playlist_name, collaborative_status]) and collaborative_status == True or collaborative_status == False:
            playlist = self.get_playlist_by_name(playlist_name)
            playlist_id = playlist.id
            if playlist.public == True:
                json ={
                    'collaborative': collaborative_status,
                }   
                new_response.put(f'/playlists/{playlist_id}', self.api.token, json=json)   
      
    def get_playlist_tracks(self, playlist_name, limit=100):
        """
        Returns list of tracks (class Track)
        """
        if playlist_name:
            playlist = self.get_playlist_by_name(playlist_name)
            track_total = playlist.tracks['total']
            offset = 0
            tracks = []
            next_url = ''
            while offset < track_total:
                if not next_url:
                    response = new_response.get(f'/playlists/{playlist.id}/tracks', self.api.token)
                else:
                    response = new_response.get('', self.api.token, next=next_url)
                next_url = response['next']
                for song in response['items']:
                    if song['track']:
                        tracks.append(Track(song['track']))
                offset += limit
            return tracks

    def get_song_from_playlist(self, playlist_name, track_name, track_artist='', limit=100):
        playlist = self.get_playlist_by_name(playlist_name)
        if not playlist:
            print(f"Playlist '{playlist_name}' not found.")
            return None

        track_total = playlist.tracks['total']
        offset = 0
        next_url = ''

        while offset < track_total:
            if not next_url:
                response = new_response.get(f'/playlists/{playlist.id}/tracks', self.api.token)
            else:
                response = new_response.get('', self.api.token, next=next_url)

            for song in response['items']:
                if song['track']['name'].lower() == track_name.lower():
                    if not track_artist or any(
                        artist['name'].lower() == track_artist.lower() for artist in song['track']['artists']
                    ):
                        return Track(song['track'])

            offset += limit
            next_url = response.get('next', '')

        print(f"Song '{track_name}' by '{track_artist}' not found in playlist '{playlist_name}'.")
        return None
      
    def add_songs_to_playlist(self, playlist_name='', song_uri_list=[], position_to_add_songs = None, playlist_id=''):
        """
        Adds song(s) to a playlist
        songs_list is an input of tuple (song name, song artist) 
        position_to_add_songs default is None which is at the end of the playlist, set to 0 for first position
        """
        if playlist_id:
            json = {'uris': song_uri_list}
            response = new_response.post(f'/playlists/{playlist_id}/tracks', self.api.token, json=json)
            return response
        
        if playlist_name and song_uri_list:
            playlist = self.get_playlist_by_name(playlist_name)
            json = {'uris': song_uri_list}
            if isinstance(position_to_add_songs, int) and position_to_add_songs <= playlist.tracks['total'] - 1:
                json['position'] = position_to_add_songs
            response = new_response.post(f'/playlists/{playlist.id}/tracks', self.api.token, json=json)
            return response
      
    def remove_song_from_playlist(self, playlist_name='', song_list_uri=[], song_name='', song_artist=''):
        playlist = self.get_playlist_by_name(playlist_name)
        if song_list_uri:
            json = {'uris': song_list_uri}
        else:
            track = self.get_song_from_playlist(playlist_name,track_name=song_name, track_artist=song_artist)
            if not track:
                return    
            json = {'tracks': [{'uri': track.uri}]}

        response = new_response.delete(f'/playlists/{playlist.id}/tracks', self.api.token, json=json)
        return response     
      
    def create_playlist(self, playlist_name, playlist_description, public_status=True):
            """
            Creates a playlist in the authenticated user's account
            """
            self.api.token_expired()
            if any(playlist_name):
                json ={
                    'name': playlist_name,
                    'description': playlist_description,
                    'public' : public_status
                }
                response = new_response.post(f'/users/{self.id()}/playlists', self.api.token,json=json, application_json_headers_bool=True)
                return response          
        
    def duplicate_playlist(self, playlist_name):
        playlist = self.get_playlist_by_name(playlist_name)
        if playlist is None:
            print(f"Playlist '{playlist_name}' not found.")
            return None

        tracks = self.get_playlist_tracks(playlist_name)
        song_uri_list = [f'spotify:track:{item.id}' for item in tracks]

        new_playlist_name = f'{playlist_name} copy'
        new_playlist = self.create_playlist(new_playlist_name, playlist.description)

        chunk_size = 100
        for i in range(0, len(song_uri_list), chunk_size):
            chunk = song_uri_list[i:i + chunk_size]
            self.add_songs_to_playlist(song_uri_list=chunk, playlist_id=new_playlist['id'])

    def shuffle_playlist(self, playlist_name):      
        playlist = self.get_playlist_by_name(playlist_name)
        if playlist is None:
            print(f"Playlist '{playlist_name}' not found.")
            return None
        
        song_uri_list = []
        tracks = self.get_playlist_tracks(playlist_name)
        song_uri_list = [{'uri': f'spotify:track:{item.id}'} for item in tracks]
        shuffle_song_uri_list = [f'spotify:track:{item.id}' for item in tracks] 
        
        chunk_size = 100
        for i in range(0, len(song_uri_list), chunk_size):
            chunk = song_uri_list[i:i + chunk_size]
            json = {'tracks': chunk}
            new_response.delete(f'/playlists/{playlist.id}/tracks', self.api.token, json=json)
            
        random.shuffle(shuffle_song_uri_list)
        
        chunk_size2 = 100
        for i in range(0, len(shuffle_song_uri_list), chunk_size2):
            chunk2 = shuffle_song_uri_list[i:i + chunk_size2]
            self.add_songs_to_playlist(song_uri_list=chunk2, playlist_id=playlist.id)

    def get_playlist_count(self):
        """
        Returns the number of playlists owned or followed by a Spotify user
        """
        response = new_response.get(f'/users/{self.id()}/playlists', self.api.token)
        return response['total']

    def create_qr_image_for_playlist(self, playlistname):
        """
        Creates a qr code that gives the link of a playlist
        """
        playlist_link = self.get_playlist_by_name(playlistname).external_urls['spotify']
        img = qrcode.make(playlist_link)
        img.save('qr_images/' + playlistname + '.png')
        return