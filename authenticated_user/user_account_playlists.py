from item import playlist

class UserAccountPlaylists:
    """"
    Gives an authenticated user access to interact with their own playlists
    """
    def __init__(self, spotifyAPI):
        self.current_users_playlists = []
        self.add_playlists(spotifyAPI)
        self.spotify = spotifyAPI.sp
        self.user_id = self.spotify.current_user()['id']

    def add_playlists(self, spotifyapi):
        """
        adds all user playlists to self.current_users_playlists
        """
        results = spotifyapi.sp.current_user_playlists()
        self.current_users_playlists = results['items']

    def get_playlist_by_name(self, name):
        """"
        returns a playlist object
        """
        for i in self.current_users_playlists:
            if i['name'] == name:
                return playlist.Playlist(i)
        raise ValueError(f"Playlist with name '{name}' not found.")

    def create_playlist(self, name, description):
        """"
        Creates a playlist in the authenticated users account
        """
        try:
            new_playlist = self.spotify.user_playlist_create(
                user=self.user_id, name=name, description=description)
            return playlist.Playlist(new_playlist) 
        except Exception as e:
            raise ValueError(f"Error creating playlist: {str(e)}")
  
    def update_playlist_name(self, old_playlist_name, new_playlist_name):
        """"
        Updates a users playlist name
        """
        try:
            playlist = self.get_playlist_by_name(old_playlist_name)
            self.spotify.user_playlist_change_details(
                user=self.user_id, playlist_id=playlist.id, name=new_playlist_name)
            print(
                f"Playlist name updated: {old_playlist_name} -> {new_playlist_name}")
        except ValueError:
            print(f"Error: Playlist '{old_playlist_name}' not found.")
        except Exception as e:
            print(f"Error updating playlist name: {str(e)}")

    def update_playlist_description(self, playlist_name, new_decription):
        try:
            playlist = self.get_playlist_by_name(playlist_name)
            old_description = playlist.description
            self.spotify.user_playlist_change_details(
                user=self.user_id, playlist_id=playlist.id, description=new_decription)
            print(
                f"Playlist description updated: {old_description} -> {new_decription}")
        except ValueError:
            print(f"Error: Playlist '{playlist_name}' not found.")
        except Exception as e:
            print(f"Error updating playlist description: {str(e)}")

    def update_playlist_visibility(self, playlist_name, visibility_bool):
        if not isinstance(visibility_bool, bool):
            print(f"Error: 'visibility_bool' parameter must be a boolean value")
        try:
            playlist = self.get_playlist_by_name(playlist_name)
            self.spotify.user_playlist_change_details(
                user=self.user_id, playlist_id=playlist.id, public=visibility_bool)
        except ValueError:
            print(f"Error: Playlist '{playlist_name}' not found.")
        except Exception as e:
            print(f"Error updating playlist visibility: {str(e)}")

            # print(results.keys())
        # print([playlist['name'] for playlist in results['items']])
        # print(results['items'][4]['description'])
        # x = [playlist['name'] for playlist in results['items']]
        # print(x)
        # ['collaborative', 'description', 'external_urls', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri'])
        # print(results)

    def find_current_users_playlists_names(self):
        self.current_users_playlists_names = []
        for playlist in self.current_users_playlists:
            self.current_users_playlists_names.append(playlist["name"])
        return self.current_users_playlists_names

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
