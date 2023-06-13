from item.track import Track
from authenticated_user.innit import AuthenticatedUser


class CurrentTrackUpdater(AuthenticatedUser):
    """"
    Initializes the access to an authenticated user's current state
    """
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        super().__init__(client_id=client_id, client_secret=client_secret,
                         redirect_uri=redirect_uri, scope=scope)
        self.current_state = self.sp.current_playback()
        
    def pause(self):
        """"
        Pauses the user's music
        """
        if self.sp.current_playback() is not None:
            play_state = self.current_state['is_playing']
            if play_state == False:
                self.sp.start_playback()
            else:
                self.sp.pause_playback()

    
    def resume(self):
        """"
        Resumes the user's music
        """
        self.pause()

    
    def skip(self):
        """"
        Skips the current song the user is listening to
        """
        if self.current_state is not None:
           self.sp.next_track()

    def shuffle(self):
        """
        Enables/disables shuffle
        """
        if self.current_state is not None:
            shuffle_state = self.current_state['shuffle_state']
            if shuffle_state == False:
                self.sp.shuffle(True)
            else:
                self.sp.shuffle(False)
        
    def repeat(self):
        """
        Enables/disables repeat
        """
        if self.current_state is not None:
            repeat_state = self.current_state['repeat_state']
            if repeat_state == 'off':
                self.sp.repeat('context')
            elif repeat_state == 'context':
                self.sp.repeat('track')
            else:
                self.sp.repeat('off')
        
    def volume(self, volume):
        """
        Adjust music volume
        """
        if self.current_state is not None:
            if 0 <= volume <=100:
                self.sp.volume(volume)
            else:
                raise ValueError("Volume input must be between 0-100")

    def previous_track(self):
        """
        Stops current song and plays previous song
        """
        if self.current_state is not None:
            self.sp.previous_track()
    
    def play_track(self, track_name, track_artist = ""):
        """
        Play a track given a track name and optional track artist
        """
        if self.current_state is not None:
            query = f'track:"{track_name}" artist:"{track_artist}"'
            results = self.sp.search(q=query, type='track', limit=1)
            items = results.get('tracks', {}).get('items', [])
            if len(items) != 0:
                self.sp.start_playback(uris=[Track(items[0]).uri])
            else:
                raise ValueError("Could not find a song")
    
    def add_track_to_queue(self, track_name, track_artist = ""):
        """
        Adds a track given a track name and optional track artist to queue
        """
        if self.current_state is not None:
            query = f'track:"{track_name}" artist:"{track_artist}"'
            results = self.sp.search(q=query, type='track', limit=1)
            items = results.get('tracks', {}).get('items', [])
            if len(items) != 0:
                self.sp.add_to_queue(uri=Track(items[0]).uri)
            else:
                raise ValueError("Could not find a song")
       
    
    def play_playlist(self, playlist_name="", playlist_uri="", playlist_link=""):
        """
        Plays a playlist given a playlist name(if playlist exists in users library), 
        playlist uri or playlist link
        """
        if self.current_state is not None and any([playlist_name, playlist_uri, playlist_link]):
            if playlist_uri:
                self.sp.start_playback(context_uri=playlist_uri)
            elif playlist_link:
                playlist_id = playlist_link.split('/')[-1]
                self.sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
            else:
                playlists = self.sp.current_user_playlists()
                for playlist in playlists['items']:
                    if str(playlist['name']).strip().lower().replace(" ", "") == playlist_name.strip().lower().replace(" ", ""):
                        self.sp.start_playback(context_uri=playlist['uri'])
                        return
                raise ValueError("playlist not found")
    
                



    
        
    

    
    
    