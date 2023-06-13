from item import playlist
from item.database import Database
from authenticated_user.innit import AuthenticatedUser


class UserAccountPlaylists(AuthenticatedUser):
    """"
    Gives an authenticated user access to interact with their own playlists
    """
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        super().__init__(client_id=client_id, client_secret=client_secret,
                         redirect_uri=redirect_uri, scope=scope)
        self.spotify = self.sp
        self.user_id = self.spotify.current_user()['id']
        self.add_playlists(self.sp)
        
        
    def add_playlists(self, spotifyapi):
        """
        adds all user playlists to self.current_users_playlists
        """
        results = spotifyapi.current_user_playlists()
        self.current_users_playlists = results['items']
        
        
    def get_playlist_by_name(self, name):
        """"
        returns a playlist object
        """
        for i in self.current_users_playlists:
            if i['name'].strip().lower() == name.strip().lower():
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
        # try:
        playlist = self.get_playlist_by_name(old_playlist_name)
        self.spotify.user_playlist_change_details(
            user=self.user_id, playlist_id=playlist.id, name=new_playlist_name)
        print(
            f"Playlist name updated: {old_playlist_name} -> {new_playlist_name}")
        # except ValueError:
        #     raise ValueError(f"Error: Playlist '{old_playlist_name}' not found.")
        # except Exception as e:
        #     raise Exception(f"Error updating playlist name: {str(e)}")

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
    
    
    def add_songs_to_db(self, playlist_name, database_name):
        playlist_id = self.get_playlist_by_name(playlist_name).id
        db = Database(database_name)
        db.create_table()
        
        offset = 0
        limit = 100
        total_tracks = 0
        tracks = []

        while True:
            results = self.spotify.playlist_tracks(playlist_id, offset=offset, limit=limit)
            tracks.extend(results['items'])
            offset += limit
            total_tracks += len(results['items'])

            if total_tracks >= results['total']:
                break
 
        #####ADDING NONE TYPES SOMEHOW
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

    
    
    
    
    
    
    
    
    
    
    
    
    
    # def add_songs_to_db(self, playlist_name, database_name):
        
    #     playlist_id = self.get_playlist_by_name(playlist_name).id
    #     db = Database(database_name)
    #     db.create_table()
    #     results = self.spotify.playlist_tracks(playlist_id)
    #     tracks = results['items']
        
    #     while results['next']:
    #         results = self.spotify.next(results)
    #         tracks.extend(results['items'])
            
    #     playlist_id = db.create_playlist(playlist_name)
    #     count = 0
    #     for track in tracks:
    #         song_name = track['track']['name']
    #         artist = track['track']['artists'][0]['name']
    #         album = track['track']['album']['name']
    #         count += 1
           
    #         db.store_song_in_playlist(playlist_id, song_name, artist, album)
    #     print(count)        
            
            
            
            
            
            
            
            
            
    
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

