from .__innit__ import API
from src.item.response import new_response

class MusicControls:
    def __init__(self):
        self.api = API()
        
    def playback_state(self):
        """
        Returns playback state
        """
        self.api.token_expired()
        response = new_response.get('/me/player', self.api.token)
        if response == 204:
            print('There is no current playback')
            return
        else:
            return response
        
    def current_track_info(self):
        """
        Prints current track info to the terminal
        """
        current_state = self.playback_state()
        if current_state is not None:
            current_track = new_response.get('/me/player/currently-playing',  self.api.token)

            artist_names = [artist['name'] for artist in current_track['item']['artists']]
            device_name = current_state['device']['name']
            progress_ms = current_track["progress_ms"]
            duration_ms = current_track["item"]["duration_ms"]
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

            # Calculate the percentage of progress
            progress_percent = (progress_ms / duration_ms) * 100

            # Create a progress bar
            bar_length = 40 # Length of the progress bar
            # filled_length = int(bar_length * progress_percent / 100)
            # bar = '|' * filled_length + '-' * (bar_length - filled_length)
            filled_length = int(bar_length * progress_percent / 100)
            bar = '\u2588' * filled_length + '\u2591' * (bar_length - filled_length)


            print("Playback State:")
            print(f"Is Playing: {current_state['is_playing']}")
            print(f"Device: {device_name}")
            print(f"Progress: {progress_time} out of {duration_time}")
            print(f"Currently Playing: {current_track['item']['name']} by {', '.join(artist_names)}")
            print(f"Progress Bar: [{bar}]")
        else:
            print("No playback state found.")
 
    def toggle_pause_play(self):
        """
        Toggles pause/play
        """
        current_state = self.playback_state()
        if current_state is not None:
            if not current_state['is_playing']:
                new_response.put('/me/player/play', self.api.token)
                print("Resuming music")  
            else:
                new_response.put('/me/player/pause', self.api.token)
                print("Paused music")
                
    def play(self):
        """"
        Resumes the user's music
        """   
        current_state = self.playback_state()
        if current_state is not None:
            if not current_state['is_playing']:
                new_response.put('/me/player/play', self.api.token)
                print("Resuming music")    
    
    def pause(self):
        """"
        Pauses the user's music
        """
        current_state = self.playback_state()
        if current_state is not None:
            if current_state['is_playing']:
                new_response.put('/me/player/pause', self.api.token)
                print("Paused music")
    
    def skip(self):
        """"
        Skips the current song the user is listening to
        """
        current_state = self.playback_state()
        if current_state is not None:
            new_response.post('/me/player/next',self.api.token)
            print('skipping song')
            
    def previous_track(self):
        """
        Stops current song and plays previous song
        """
        current_state = self.playback_state()
        if current_state is not None:
            new_response.post('/me/player/previous', self.api.token)
            
    def start_at(self, time):
        """
        Input is time where you want the song to be at in milliseconds.
        Supports inputs like <0:32> and <32>
        """
        current_state = self.playback_state()
        if current_state is not None:
            if ':' in str(time):
                convert_time_to_ms = (int(time.split(':')[0])*60  +  int(time.split(':')[1])) * 1000
                new_response.put(f'/me/player/seek?position_ms={convert_time_to_ms}', self.api.token)
            else:
                convert_time_to_ms = int(time) * 1000
                new_response.put(f'/me/player/seek?position_ms={convert_time_to_ms}', self.api.token)  
   
    def repeat(self):
        """
        Enables/disables repeat
        """
        current_state = self.playback_state()
        if current_state is not None:
            repeat_state = current_state['repeat_state']
            if repeat_state == 'off':
                new_response.put('/me/player/repeat?state=context', self.api.token)
                print('Enabled repeat')
            elif repeat_state == 'context':
                new_response.put('/me/player/repeat?state=track', self.api.token)
                print('Enabled repeat one')
            else:
                new_response.put('/me/player/repeat?state=off', self.api.token)
                print('Disabled repeat')
    
    def volume(self, volume):
        """
        Adjust music volume
        """
        current_state = self.playback_state()
        if current_state is not None:
            if 0 <= int(volume) <=100:
                new_response.put(f'/me/player/volume?volume_percent={volume}', self.api.token)
                print(f'volume is at {volume}%')
            else:
                print("Volume input must be between 0-100")

    def shuffle(self):
        """
        Enables/disables shuffle
        """
        current_state = self.playback_state()
        if current_state is not None:
            new_response.put(f'/me/player/shuffle?state={not current_state["shuffle_state"]}', self.api.token)
            if current_state["shuffle_state"]:
                print('Disabled shuffle')
            else:
                print('Enabled shuffle')

    def recently_played(self, amount=20):
        """
        Prints the song names and artists of the amount recently played
        """
        current_state = self.playback_state()
        if current_state is not None:
            respo = new_response.get('/me/player/recently-played', self.api.token)
            if respo != 204:
                for item in respo['items']:
                    song = item['track']['name']
                    artist_names = ', '.join([artist['name'] for artist in item['track']['artists']])
                    print(f"{song} by {artist_names}")

    def play_track(self, track_name, track_artist = ""):
        """
        Play a track given a track name and optional track artist
        "album", "artist", "playlist", "track", "show", "episode", "audiobook"
        """
        current_state = self.playback_state()
        if current_state is not None:
            params = {
                "q": f"remaster%20track:{track_name}",
                "type": ["track"],
            }
            if track_artist:
                params["q"] += f"%20artist:{track_artist}"
            respo = new_response.get("/search", self.api.token, params=params) # search for item in search
            if respo != 204:
                track_uri = respo['tracks']['items'][0]['uri']
                json = {'uris' : [str(track_uri)]}           
                new_response.put('/me/player/play', self.api.token, json=json) #start.resume playback in player 
           
    def search_for_track(self, track_name, track_artist = ""):
        current_state = self.playback_state()
        if current_state is not None:
            params = {
                "q": f"remaster%20track:{track_name}",
                "type": ["track"],
            }
            if track_artist:
                params["q"] += f"%20artist:{track_artist}"
            respo = new_response.get("/search", self.api.token, params=params)
            if respo != 204:
                for item in respo['tracks']['items']:
                    song = item['name']
                    artist_names = ', '.join([artist_name['name'] for artist_name in item['artists']])
                    print(f"{song} by {artist_names}")

    def queue(self, track_name, track_artist = ""):
        """
        Adds a track given a track name and optional track artist to queue
        """
        current_state = self.playback_state()
        if current_state is not None:
            params = {
                "q": f"remaster%20track:{track_name}",
                "type": ["track"],
            }
            if track_artist:
                params["q"] += f"%20artist:{track_artist}"
            respo = new_response.get("/search", self.api.token, params=params)
            if respo != 204:
                uri = respo['tracks']['items'][0]['uri']
                song = respo['tracks']['items'][0]['name']
                artist_names = ', '.join([artist_name['name'] for artist_name in respo['tracks']['items'][0]['artists']])
                new_response.post(f'/me/player/queue?uri={uri}', self.api.token)
                print(f'{song} by {artist_names} has been queued')
                return respo
            
    def play_playlist(self, playlist_name="", playlist_uri="", playlist_link=""):
        """
        Plays a playlist given a playlist name(if playlist exists in users library), 
        playlist uri or playlist link
        """
        current_state = self.playback_state()
        if current_state is not None and any([playlist_name, playlist_uri, playlist_link]):
            if playlist_uri:
                if 'spotify:track:' in playlist_uri:
                    json = {'context_uri': playlist_uri}
                else:
                    json = {'context_uri': 'spotify:playlist:' + playlist_uri}
                print(json)
                new_response.put('/me/player/play', self.api.token, json=json)
            elif playlist_link:
                json = {'context_uri': playlist_link}
                new_response.put('/me/player/play', self.api.token, json=json)
            elif playlist_name:
                params = {
                    'limit': 50
                }
                get_users_playlists = new_response.get('/me/playlists', self.api.token, params)
                for i in get_users_playlists['items']:
                    if i['name'].lower() == playlist_name:
                        playlist_uri = i['uri']
                if playlist_uri:
                    json = {'context_uri': playlist_uri}
                    new_response.put('/me/player/play', self.api.token, json=json)
            else:
                print('no valid input was given')
       
       
