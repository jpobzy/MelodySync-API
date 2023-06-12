from authenticated_user import user_account_playlists
import time

class AuthenticatedUserPlaylistTests():
    def run_tests(spotifyAPI):
        # print("BEGINNING TEST RUNS for user_account_playlist")
        playlist_obj = user_account_playlists.UserAccountPlaylists(spotifyAPI)
        # playlist_tests.individual_expected_playlist_in_my_account(playlist_obj)
        # playlist_tests.multiple_expected_playlist_in_my_account(playlist_obj)
        AuthenticatedUserPlaylistTests.create_playlist_test(playlist_obj)
        
    def individual_expected_playlist_in_my_account(playlist_obj):
        """
        Checks that a specific playlist name exists in all of my playlists
        """
        actual_name1 = playlist_obj.get_playlist_by_name("Chill V3").name
        expected_name1 = "Chill V3"
        assert actual_name1 == expected_name1, f"get_playlist_by_name DID NOT MATCH, Expected: {expected_name1}, Actual: {actual_name1}"
        
    def multiple_expected_playlist_in_my_account(playlist_obj):
        """
        
        """
        expected_users_playlists = ['Chill V6', 'Chill v5', 'Songs To Play In The Gym by RapTV', 'Requests', 'Chill', 'Chill V2', 'Chill V3', 'Chill V4', 'Chill v5 (old)', 'Christmas shit', 'Hs1', 'Hs2', 'Hs3', 'Hs4', 'L4D Frag music ', 'Mellow', 'Ms/Hs fav ', 'Ms/Hs V1', 'Old shit', '🅿️', 'Radio shit', 'Radio shit V0.25', 'Radio shit V0.5', 'Radio shit V0.75', 'Random rap in my library V1', 'Random rap in my library V2', 'Random rap in my library V3', 'Random rap in my library V4', 'Random rap in my library V5', 'Santa szn', 'Spooky szn', 'Sad Boi Hours', "Let's Get Railed", 'free thug', 'Springter', 'Radio shitv1', 'best xmas playlist ', '😨', '🎉🎊🎉', 'Urbano Latino', '🚹♿️🚺', '🍸🍸🍸', 'Shower Shit']
        for playlist_name in expected_users_playlists:
            assert playlist_name in playlist_obj.find_current_users_playlists_names(), f"Playlist name '{playlist_name}' not found in expected users playlists"

    def create_playlist_test(playlist_obj):
        """
        Creates a playlist then waits 9 seconds to delete it
        """
        playlist_name = "ඞඞඞ"
        playlist_description =  "amogus"
        new_playlist = playlist_obj.create_playlist(playlist_name, playlist_description)
        assert playlist_name == new_playlist.name, f"Created playlist name was not found in playlist library, Expected [{playlist_name}], Acutual [{new_playlist.name}]"
        time.sleep(9)
        playlist_obj.spotify.current_user_unfollow_playlist(new_playlist.id)

    def update_playlist_name_test(playlist_obj):
        """
        Creates 
        """
        playlist_name = "playlist A"
        playlist_description =  "update_playlist_name_test description"
        new_playlist = playlist_obj.create_playlist(playlist_name, playlist_description)
        assert playlist_name == new_playlist.name, f"Created playlist name was not found in playlist library, Expected [{playlist_name}], Acutual [{new_playlist.name}]"
        
        new_playlist_name = "playlist B"
        playlist_obj.update_playlist_name(playlist_name, new_playlist_name)
        assert new_playlist_name == new_playlist.name, f"Updated playlist name was not found in playlist library, Expected [{playlist_name}], Acutual [{new_playlist.name}]"
        
        
        time.sleep(9)
        playlist_obj.spotify.current_user_unfollow_playlist(new_playlist.id)       

    def update_playlist_description_test(playlist_obj):
        pass

    def update_playlist_visibility_test(playlist_obj):
        pass

    
        
        
                
        # playlist_test(playlist_obj=playlist_obj)
        # playlist_obj.change_playlist_visibility("hello world", False)
        # track_names = x.get_track_names()
        # print(track_names)

        # playlist_obj.get_playlist_by_name("Chill V3")['name']
        
        # assert playlist_obj.get_playlist_by_name("Chill V3").name == expected_name1, f"get_playlist_by_name DID NOT MATCH, Expected: {expected_name1}, Actual: {playlist_obj.get_playlist_by_name('Chill V3').name}"
        
        # assert playlist_obj.current_users_playlists_names == []
        # assert len(playlist_obj.current_users_playlists_names) == 0,f"len of playlist_obj.current_users_playlists_names DID NOT MATCH. Expected: {0}, Actual: {len(playlist_obj.current_users_playlists_names)}"
        # for i in range(len(expected_users_playlists)):
        #     assert expected_users_playlists[i] == playlist_obj.find_current_users_playlists_names()[i], f"find_current_users_playlists_names DID NOT MATCH. Expected: {expected_users_playlists[i]}, Actual: {playlist_obj.find_current_users_playlists_names()[i]}"
        # assert len(playlist_obj.current_users_playlists_names) != 0,f"len of playlist_obj.current_users_playlists_names DID NOT MATCH. Expected: {0}, Actual: {len(playlist_obj.current_users_playlists_names)}"


        


def playlist_test(playlist_obj):
    """"
    creates a playlist if the name doesnt exist
    """
    if not playlist_obj.get_playlist_by_name("hello world"):
        print("playlist not found, creating playlist...") 
        playlist_obj.create_playlist("hello world", "this is the description")
        
    # playlist_obj.change_playlist_name("hello world", "goodbye world")
    # playlist_obj.change_playlist_description("hello world", "new description")
    