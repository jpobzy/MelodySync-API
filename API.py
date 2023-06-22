import json
from item.playlist import Playlist
from item.track import Track
import random
from item.database import Database
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time


class API:
    def __init__(self):
        self.authenticate()
    
    def authenticate(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
        with open('scopes/dev_scopes.json') as scopes_file:  # or use 'scopes/private_scopes.json' or 'scopes/public_scopes.json'
            scopes = json.load(scopes_file)

        client_id = config['client_id']
        client_secret = config['client_secret']
        redirect_uri = config['redirect_uri']
        scope = scopes['scope']

        sp_oauth  = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                        redirect_uri=redirect_uri, scope=scope)
        self.spotify = spotipy.Spotify(auth_manager=sp_oauth)
        
    def get_user_display_name(self):
        """"
        Returns current authenticated users display name
        """
        return self.spotify.current_user()['display_name']

    def get_user_id(self):
        """"
        Returns current authenticated users Id
        """
        return self.spotify.current_user()['id']

    def get_get_user_profile_image_url(self):
        """"
        Returns current authenticated users profile image url
        """
        return self.spotify.current_user()['images'][-1]['url']

    def get_user_uri(self):
        """"
        Returns current authenticated user's uri
        """
        return self.spotify.current_user()["uri"]
    
    def get_current_state(self):
            self.current_state = self.spotify.current_playback()    
    
    def pause(self):
        """"
        Pauses the user's music
        """
        current_state = self.spotify.current_playback()
        if current_state is not None:
            play_state = current_state['is_playing']
            if play_state:
                self.spotify.pause_playback()

    def play(self):
        """"
        Resumes the user's music
        """
        current_state = self.spotify.current_playback()
        if current_state is not None:
            play_state = current_state['is_playing']
            if not play_state:
                self.spotify.start_playback()
    
    def skip(self):
        """"
        Skips the current song the user is listening to
        """
        if self.current_state is not None:
           self.spotify.next_track()

    def shuffle(self):
        """
        Enables/disables shuffle
        """
        if self.current_state is not None:
            shuffle_state = self.current_state['shuffle_state']
            self.spotify.shuffle(not shuffle_state)
            self.current_state['shuffle_state'] = not shuffle_state
   
    def repeat(self):
        """
        Enables/disables repeat
        """
        if self.current_state is not None:
            repeat_state = self.current_state['repeat_state']
            if repeat_state == 'off':
                self.spotify.repeat('context')
                self.current_state['repeat_state'] = 'context'
            elif repeat_state == 'context':
                self.spotify.repeat('track')
                self.current_state['repeat_state'] = 'track'
            else:
                self.spotify.repeat('off')
                self.current_state['repeat_state'] = 'off'
    
    def volume(self, volume):
        """
        Adjust music volume
        """
        if self.current_state is not None:
            if 0 <= volume <=100:
                self.spotify.volume(volume)
            else:
                print("Volume input must be between 0-100")
                # raise ValueError("Volume input must be between 0-100")

    def play_previous_track(self):
        """
        Stops current song and plays previous song
        """
        if self.current_state is not None:
            self.spotify.previous_track()

    def play_track(self, track_name, track_artist = ""):
        """
        Play a track given a track name and optional track artist
        """
        if self.current_state is not None:
            query = f'track:"{track_name}" artist:"{track_artist}"'
            results = self.spotify.search(q=query, type='track', limit=1)
            items = results.get('tracks', {}).get('items', [])
            if len(items) != 0:
                self.spotify.start_playback(uris=[Track(items[0]).uri])
                
            else:
                # raise ValueError("Could not find a song")
                print("Could not find a song")

    def queue(self, track_name, track_artist = ""):
        """
        Adds a track given a track name and optional track artist to queue
        """
        if self.current_state is not None:
            query = f'track:"{track_name}" artist:"{track_artist}"'
            results = self.spotify.search(q=query, type='track', limit=1)
            items = results.get('tracks', {}).get('items', [])
            if len(items) != 0:
                self.spotify.add_to_queue(uri=Track(items[0]).uri)
            else:
                # raise ValueError("Could not find a song")
                print("Could not find a song")

    def play_playlist(self, playlist_name="", playlist_uri="", playlist_link=""):
        """
        Plays a playlist given a playlist name(if playlist exists in users library), 
        playlist uri or playlist link
        """
        if self.current_state is not None and any([playlist_name, playlist_uri, playlist_link]):
            if playlist_uri:
                self.spotify.start_playback(context_uri=playlist_uri)
            elif playlist_link:
                playlist_id = playlist_link.spotifylit('/')[-1]
                self.spotify.start_playback(context_uri=f"spotifyotify:playlist:{playlist_id}")
            else:
                playlists = self.spotify.current_user_playlists()
                for playlist in playlists['items']:
                    if str(playlist['name']).strip().lower().replace(" ", "") == playlist_name.strip().lower().replace(" ", ""):
                        self.spotify.start_playback(context_uri=playlist['uri'])
                        return
                # raise ValueError("playlist not found")
                print("playlist not found")
                
    def current_track_info(self):
        self.get_current_state()
        if self.current_state is not None:
            current_track = self.current_state['item']
            artist_names = [artist['name'] for artist in current_track['artists']]
            print(f"Currently playing {current_track['name']} by {', '.join(artist_names)}")

    def get_playlist_by_name(self, name):
        """
        Returns a playlist object
        """
        playlists = self.spotify.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'].strip().lower() == name.strip().lower():
                return Playlist(playlist)
        raise ValueError(f"Playlist with name '{name}' not found.")
            
    def create_playlist(self, name, description):
            """
            Creates a playlist in the authenticated user's account
            """
            try:
                new_playlist = self.spotify.user_playlist_create(
                    user=self.spotify.current_user()['id'], name=name, description=description)
                return Playlist(new_playlist)
            except Exception as e:
                raise ValueError(f"Error creating playlist: {str(e)}")

    def update_playlist_name(self, old_playlist_name, new_playlist_name):
            """
            Updates a user's playlist name
            """
            playlist = self.get_playlist_by_name(old_playlist_name)
            try:
                self.spotify.user_playlist_change_details(
                    user=self.user_id, playlist_id=playlist['id'], name=new_playlist_name)
                print(
                    f"Playlist name updated: {old_playlist_name} -> {new_playlist_name}")
            except Exception as e:
                raise Exception(f"Error updating playlist name: {str(e)}")

    def update_playlist_description(self, playlist_name, new_description):
        """
        Updates a user's playlist description
        """
        playlist = self.get_playlist_by_name(playlist_name)
        try:
            self.spotify.user_playlist_change_details(
                user=self.user_id, playlist_id=playlist['id'], description=new_description)
            print(
                f"Playlist description updated: {playlist['description']} -> {new_description}")
        except Exception as e:
            raise Exception(f"Error updating playlist description: {str(e)}")

    def update_playlist_visibility(self, playlist_name, visibility_bool):
        """
        Updates a user's playlist visibility (public/private)
        """
        if not isinstance(visibility_bool, bool):
            raise ValueError("'visibility_bool' parameter must be a boolean value")
        playlist = self.get_playlist_by_name(playlist_name)
        try:
            self.spotify.user_playlist_change_details(
                user=self.user_id, playlist_id=playlist['id'], public=visibility_bool)
        except Exception as e:
            raise Exception(f"Error updating playlist visibility: {str(e)}")

    def get_playlist_tracks(self, playlist_name, return_type=None):
        playlist = self.get_playlist_by_name(playlist_name)
        track_list = []
        
        if playlist is None:
            print(f"Playlist '{playlist_name}' not found.")
            return None

        playlist_id = playlist.id
        total_tracks = playlist.tracks['total']
        
        # Retrieve tracks in batches of 100 using pagination
        offset = 0
        limit = 100
        while offset < total_tracks:
            tracks = self.spotify.playlist_tracks(playlist_id, offset=offset, limit=limit)
            for item in tracks['items']:
                track_list.append(Track(item['track']))
            
            offset += limit
        
        return track_list

    def duplicate_playlist(self, playlist_name):
        playlist = self.get_playlist_by_name(playlist_name)
        track_list = []
        
        if playlist is None:
            print(f"Playlist '{playlist_name}' not found.")
            return None

        playlist_id = playlist.id
        total_tracks = playlist.tracks['total']
        
        new_playlist = self.create_playlist(f"{playlist_name} copy", playlist.description)
        offset = 0
        limit = 100
        while offset < total_tracks:
            tracks = self.spotify.playlist_tracks(playlist_id, offset=offset, limit=limit)
            for item in tracks['items']:
                track_list.append(Track(item['track']).id)
            self.spotify.playlist_add_items(new_playlist.id, track_list)
            track_list = []
            offset += limit

    def shuffle_playlist(self, playlist_name):
        playlist = self.get_playlist_by_name(playlist_name)

        if playlist is None:
            print(f"Playlist '{playlist_name}' not found.")
            return

        playlist_id = playlist.id

        # Retrieve all track URIs from the playlist
        track_uris = []
        offset = 0
        limit = 100
        total_tracks = playlist.tracks['total']
        
        while offset < total_tracks:
            items = self.spotify.playlist_items(playlist_id, offset=offset, limit=limit, fields='items(track(uri))')
            track_uris.extend([item['track']['uri'] for item in items['items']])
            offset += limit

        # Shuffle the track URIs
        random.shuffle(track_uris)

        # Remove all existing tracks from the playlist
        self.spotify.playlist_replace_items(playlist_id, [])

        # Add the shuffled tracks back to the playlist in batches of 100
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i+100]
            self.spotify.playlist_add_items(playlist_id, batch)

        print(f"Playlist '{playlist_name}' shuffled successfully.")
                
    def get_song_recommendations(self, playlist_name, num_seeds=1, limit=10):
        # Get playlist ID
        if num_seeds > 5:
            print("max number of seeds is 5")
            return
        playlist = self.get_playlist_by_name(playlist_name)
        if playlist is None:
            print(f"Playlist '{playlist_name}' not found.")
            return
        
        playlist_id = playlist.id
        
        try:
            # Get tracks from the playlist
            tracks = self.spotify.playlist_tracks(playlist_id, limit=num_seeds)
            seed_track_uris = [track['track']['uri'] for track in tracks['items']]
            
            # Get recommendations based on the seed tracks
            recommendations = self.spotify.recommendations(seed_tracks=seed_track_uris, limit=limit)
            
            # Print the recommended tracks
            for track in recommendations['tracks']:
                track_name = track['name']
                artists = ", ".join([artist['name'] for artist in track['artists']])
                print(track_name, "-", artists)
                
        except spotipy.exceptions.SpotifyException as e:
            print(f"Error retrieving recommendations: {str(e)}")

    def playback_state(self):
        self.get_current_state()

        if self.current_state is not None:
            is_playing = self.current_state["is_playing"]
            device_name = self.current_state["device"]["name"]
            progress_ms = self.current_state["progress_ms"]
            duration_ms = self.current_state["item"]["duration_ms"]
            item = self.current_state["item"]
            track_name = item["name"]
            artist_names = [artist["name"] for artist in item["artists"]]

            # Convert progress_ms and duration_ms to seconds
            progress_seconds = progress_ms // 1000
            duration_seconds = duration_ms // 1000

            # Format progress time as MM:SS
            progress_minutes = progress_seconds // 60
            progress_seconds %= 60
            progress_time = f"{progress_minutes}:{progress_seconds:02d}"

            # Format duration time as MM:SS
            duration_minutes = duration_seconds // 60
            duration_seconds %= 60
            duration_time = f"{duration_minutes}:{duration_seconds:02d}"

            print("Playback State:")
            print(f"Is Playing: {is_playing}")
            print(f"Device: {device_name}")
            print(f"Progress: {progress_time} out of {duration_time}")
            print(f"Currently Playing: {track_name} by {', '.join(artist_names)}")
        else:
            print("No playback state found.")

    def add_playlist_to_database(self, playlist_name, database_name):
        """
        Adds songs from a playlist to a database
        """
        playlist_id = self.get_playlist_by_name(playlist_name).id
        if ".db" not in database_name:
            database_name = database_name
        print(database_name)
        db = Database(database_name)
        db.create_table()

        offset = 0
        limit = 100
        total_tracks = 0
        tracks = []

        while True:
            results = self.spotify.playlist_tracks(
                playlist_id, offset=offset, limit=limit)
            tracks.extend(results['items'])
            offset += limit
            total_tracks += len(results['items'])

            if total_tracks >= results['total']:
                break

        playlist_id = db.create_playlist(playlist_name)
        count = 0

        print(len(tracks))
        for track in tracks:
            try:
                if 'track' in track and 'name' in track['track']:
                    song_name = track['track']['name']
                    artist = track['track']['artists'][0]['name']
                    album = track['track']['album']['name']
                    count += 1
                    db.store_song_in_playlist(playlist_id, song_name, artist, album)
                else:
                    print('Invalid track:', track)
            except Exception as e:
                print('Error processing track:', track)
                print('Error message:', str(e))

        print('Number of songs:', count)
    
    def create_backup_library(self):
        users_playlists = self.spotify.user_playlists(self.get_user_id())
        user_playlist_id_list = [(item['id'], item['name']) for item in users_playlists['items']]
        db = Database("backup_db.db")
        db.create_backup_library() 
               
        for item in user_playlist_id_list:
            offset = 0
            limit = 100
            total_tracks = 0
            tracks = []
            
            while True:
                results = self.spotify.playlist_tracks(
                    item[0], offset=offset, limit=limit)
                tracks.extend(results['items'])
                offset += limit
                total_tracks += len(results['items'])

                if total_tracks >= results['total']:
                    break
               
            playlist_id = db.create_backup_playlist(item[1], item[0])
            count = 0
    
                                
            for track in tracks:
                try:
                    if track and 'track' in track and track['track'] and 'name' in track['track']:
                        song_name = track['track']['name']
                        artist = track['track']['artists'][0]['name']
                        track_id = track['track']['id']
                        count += 1
                                    
                        db.store_song_in_backup_playlist(playlist_id, song_name, artist, track_id)
                    else:
                        print('Invalid track:', track)
                except Exception as e:
                    print('Error processing track:', track)
                    print('Error message:', str(e))
                    

 
    


if __name__ == "__main__":
    x = API()
    x.create_backup_library()



