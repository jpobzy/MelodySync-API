import sys
import json

from authenticated_user_test.playlist_tests import AuthenticatedUserPlaylistTests
from authenticated_user_test.innit_tests import AuthenticatedUserInnitTests
from authenticated_user.current_track_updater import CurrentTrackUpdater
from authenticated_user.user_account_playlists import UserAccountPlaylists

sys.dont_write_bytecode = True  # doesn't allow pycache files to be created when running locally

from item.database import Database


def run_all_tests(spotifyAPI):
    AuthenticatedUserInnitTests.run_tests(spotifyAPI)
    AuthenticatedUserPlaylistTests.run_tests(spotifyAPI)
    print("ALL TESTS COMPLETED SUCCESSFULLY")


def main():
    with open('config.json') as config_file:
        config = json.load(config_file)
    with open('scopes/dev_scopes.json') as scopes_file:  # or use 'scopes/private_scopes.json' or 'scopes/public_scopes.json'
        scopes = json.load(scopes_file)

    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_uri = config['redirect_uri']
    scope = scopes['scope']

    # authenticated_user = AuthenticatedUser(client_id=client_id, client_secret=client_secret,
    #                                        redirect_uri=redirect_uri, scope=scope)

    # current_track_updater = CurrentTrackUpdater(client_id, client_secret, redirect_uri, scope)
    # current_track_updater.play_playlist("chillv3")

    x = UserAccountPlaylists(client_id, client_secret, redirect_uri, scope)
    # x.create_playlist("dasdas", "sadsa")
    x.add_songs_to_db("chill", "db1.db")
    # x.add_songs_to_db("chill v2", "db1.db")
    # x.add_songs_to_db("chill v3", "db1.db")
    # x = UserAccountPlaylists(spotify1)
    
    # currentTrackUpdater().pause()

    # x.add_songs_to_db("chill v3", "test.db")
    # print(x.add_songs_to_db("chill v3", "test2"))

    # print(spotify.sp.current_user())

    # spotify1 = spotifyAPI(client_id=client_id, client_secret=client_secret,redirect_uri=redirect_uri,scope=scope)
    # run_all_tests(spotify1)
    
    
    # spotify_innit_tests.spotify_innit_tests.run_tests(spotify1)
    # playlist_obj = user_account_playlist.user_account_playlist(spotify1)
    
    
    # playlisttests.run_tests(spotify1)

    # playlist_names = playlist_obj.find_current_users_playlists_names()
    # print(playlist_names)

    # print(x.find_current_users_playlists_names())
    # print(spotify_playlist(spotify1).find_current_users_playlists_names())

    # x = currentTrackUpdater(spotify1)
    # x.add_track_to_queue("champion", "nav")
    # x.resume()
    # x.previous_track()
    # current_track_playing(spotify1)
    # x.play_playlist(playlist_name="chill v3")
    
    




if __name__ == "__main__":
    main() 


# stops cache file from being created   
import os
for file in os.listdir("."):
    if file.endswith(".cache"):
        os.remove(file)

# client_id = 'a7df921d61244f76be957d95a88e86d3'
# client_secret = '50655a4429c54201ab5933556cbe5df3'
# redirect_uri = 'http://localhost:8080/callback'