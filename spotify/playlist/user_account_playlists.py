import spotipy
from spotipy.oauth2 import SpotifyOAuth
import playlist


class user_account_playlists:
    def __init__(self, spotifyAPI):
        self.current_users_playlists = []
        self.add_playlists(spotifyAPI)

    def add_playlists(self, spotifyAPI):
        results = spotifyAPI.sp.current_user_playlists()
        self.current_users_playlists = results['items']
        # print(results.keys())
        # print([playlist['name'] for playlist in results['items']])
        # print(results['items'][4]['description'])
        # x = [playlist['name'] for playlist in results['items']]
        # print(x)
        # ['collaborative', 'description', 'external_urls', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri'])
        # print(results)
    
    def get_playlist_by_name(self, name):
        for playlist in self.current_users_playlists:
            if playlist['name'] == name:
                return playlist
        raise ValueError(f"Playlist with name '{name}' not found.")



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    # def find_current_users_playlists_names(self):
    #     self.current_users_playlists_names = []
    #     for playlist in self.current_users_playlists['items']:
    #         self.current_users_playlists_names.append(playlist["name"])  
    #     return self.current_users_playlists_names



    # def get_specific_playlist(self, playlist_detection_input):
    #     users_current_playlists = self.find_current_users_playlists_names()
    #     if playlist_detection_input in users_current_playlists:
    #         ''
            
    #     my_list = ["b", "c", "a", "d"]
    #     if "a" in my_list:
    #         index_of_a = my_list.index("a")
    #         a = my_list[index_of_a]
    #         print(a) # Output: "a"

    
        
    # def get_playlist_id_from_url(self, playlist_url):
    #     return playlist_url.split("/")[-1]

    # def get_playlist_id_from_name(self, playlist_name):
    #     return playlist_name.split("/")[-1]

    # def get_playlist(self, playlist_id):

