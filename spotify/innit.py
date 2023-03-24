import spotipy
from spotipy.oauth2 import SpotifyOAuth

class spotifyAPI:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        sp_oauth  = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                        redirect_uri=redirect_uri, scope=scope)
        self.sp = spotipy.Spotify(auth_manager=sp_oauth)
        self.userinfo = self.sp.current_user()
        

    def get_display_name(self):
        return self.userinfo['display_name']
    
    def get_id(self):
        return self.userinfo['id']
    
    def get_profile_image_url(self):
        return self.userinfo['images'][-1]['url']
    
    def get_uri(self):
        return self.userinfo["uri"]