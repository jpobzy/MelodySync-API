import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlist import amogus
from playlist.playlist import Playlist


class user_account_playlists:
    def __init__(self, spotifyAPI):
        self.current_users_playlists = []
        self.add_playlists(spotifyAPI)
        self.spotify = spotifyAPI.sp
        self.user_id = self.spotify.current_user()['id']
        
    # adds all user playlists to self.current_users_playlists
    def add_playlists(self, spotifyAPI): 
        results = spotifyAPI.sp.current_user_playlists()
        self.current_users_playlists = results['items']

    
    def get_playlist_by_name(self, name):
        for playlist in self.current_users_playlists:
            if playlist['name'] == name:
                return Playlist(playlist)
        # raise ValueError(f"Playlist with name '{name}' not found.")     
        print(f"Playlist with name '{name}' not found.")
        return None
    
    def create_playlist(self, name, description):
        try:
            playlist = self.spotify.user_playlist_create(self.user_id, name, description=description)
            return playlist
        except Exception as e:
            print(f"Error creating playlist: {str(e)}")
            return None

    def change_playlist_name(self, old_playlist_name, new_playlist_name):
        try:
            playlist = self.get_playlist_by_name(old_playlist_name)
            self.spotify.user_playlist_change_details(user=self.user_id, playlist_id=playlist.id, name=new_playlist_name)
            print(f"Playlist name updated: {old_playlist_name} -> {new_playlist_name}")
        except ValueError:
            print(f"Error: Playlist '{old_playlist_name}' not found.")
        except Exception as e:
            print(f"Error updating playlist name: {str(e)}")


    def change_playlist_description(self, playlist_name, new_decription):
        try:
            playlist = self.get_playlist_by_name(playlist_name)
            old_description = playlist.description
            print(old_description)
            self.spotify.user_playlist_change_details(user=self.user_id, playlist_id=playlist.id, description=new_decription)
            print(f"Playlist description updated: {old_description} -> {new_decription}")
        except ValueError:
            print(f"Error: Playlist '{playlist_name}' not found.")
        except Exception as e:
            print(f"Error updating playlist description: {str(e)}")

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                # print(results.keys())
        # print([playlist['name'] for playlist in results['items']])
        # print(results['items'][4]['description'])
        # x = [playlist['name'] for playlist in results['items']]
        # print(x)
        # ['collaborative', 'description', 'external_urls', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri'])
        # print(results)
        

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

