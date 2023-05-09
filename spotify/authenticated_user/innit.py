import spotipy
from spotipy.oauth2 import SpotifyOAuth

class AuthenticatedUser:
    """"
    Innitializes the access to an autheticated users information
    """
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        sp_oauth  = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                        redirect_uri=redirect_uri, scope=scope)
        self.sp = spotipy.Spotify(auth_manager=sp_oauth)
        self.userinfo = self.sp.current_user()

    def get_display_name(self):
        """"
        Returns current authenticated users display name
        """
        return self.userinfo['display_name']

    def get_id(self):
        """"
        Returns current authenticated users Id
        """
        return self.userinfo['id']

    def get_profile_image_url(self):
        """"
        Returns current authenticated users profile image url
        """
        return self.userinfo['images'][-1]['url']

    def get_uri(self):
        """"
        Returns current authenticated user's uri
        """
        return self.userinfo["uri"]
