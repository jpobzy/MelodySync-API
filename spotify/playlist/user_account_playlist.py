import spotipy
from spotipy.oauth2 import SpotifyOAuth


class user_account_playlist:
    def __init__(self, spotifyAPI):
        self.current_users_playlists = spotifyAPI.sp.current_user_playlists()
        self.current_users_playlists_names = []

    def find_current_users_playlists_names(self):
        self.current_users_playlists_names = []
        for playlist in self.current_users_playlists['items']:
            self.current_users_playlists_names.append(playlist["name"])  
        return self.current_users_playlists_names


    # def get_playlist_id_from_url(self, playlist_url):
    #     return playlist_url.split("/")[-1]

    # def get_playlist_id_from_name(self, playlist_name):
    #     return playlist_name.split("/")[-1]

    # def get_playlist(self, playlist_id):

