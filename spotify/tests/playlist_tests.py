from playlist import user_account_playlists

class playlist_tests():
    def run_tests(spotifyAPI):
        # print("BEGINNING TEST RUNS for user_account_playlist")
        expected_users_playlists = ['Songs To Play In The Gym by RapTV', 'Requests', 'Chill', 'Chill V2', 'Chill V3', 'Chill V4', 'Chill v5', 'Christmas shit', 'Hs1', 'Hs2', 'Hs3', 'Hs4', 'L4D Frag music ', 'Mellow', 'Ms/Hs fav ', 'Ms/Hs V1', 'Old shit', '🅿️', 'Radio shit', 'Radio shit V0.25', 'Radio shit V0.5', 'Radio shit V0.75', 'Random rap in my library V1', 'Random rap in my library V2', 'Random rap in my library V3', 'Random rap in my library V4', 'Random rap in my library V5', 'Santa szn', 'Spooky szn', 'Sad Boi Hours', "Let's Get Railed", 'free thug', 'Springter', 'Radio shitv1', 'best xmas playlist ', '😨', '🎉🎊🎉', 'Urbano Latino', '🚹♿️🚺', '🍸🍸🍸', 'Shower Shit']
        playlist_obj = user_account_playlists.user_account_playlists(spotifyAPI)
        
        expected_name1 = "Chill V3"
        print(playlist_obj.get_playlist_by_name("Chill V3")['name'])
        # assert playlist_obj.get_playlist_by_name("Chill V3")['name'] == expected_name1, f"get_playlist_by_name DID NOT MATCH, Expected: {expected_name1}, Actual: {playlist_obj.get_playlist_by_name('Chill V3')['name']}"
        
        # assert playlist_obj.current_users_playlists_names == []
        # assert len(playlist_obj.current_users_playlists_names) == 0,f"len of playlist_obj.current_users_playlists_names DID NOT MATCH. Expected: {0}, Actual: {len(playlist_obj.current_users_playlists_names)}"
        # for i in range(len(expected_users_playlists)):
        #     assert expected_users_playlists[i] == playlist_obj.find_current_users_playlists_names()[i], f"find_current_users_playlists_names DID NOT MATCH. Expected: {expected_users_playlists[i]}, Actual: {playlist_obj.find_current_users_playlists_names()[i]}"
        # assert len(playlist_obj.current_users_playlists_names) != 0,f"len of playlist_obj.current_users_playlists_names DID NOT MATCH. Expected: {0}, Actual: {len(playlist_obj.current_users_playlists_names)}"

        
