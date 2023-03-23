import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_uri(playlist_link):
    if "spotify.com/playlist/" not in playlist_link:
        raise ValueError("Not a valid Spotify playlist link")
    playlist_id = playlist_link.split("playlist/")[1].split("?")[0]
    return "spotify:playlist:" + playlist_id

playlist_link = "https://open.spotify.com/playlist/17Pbf1N0s3A62nwgwlBXC4?si=c93cb13e40604c4c"
playlist_uri = get_spotify_uri(playlist_link)
print(playlist_uri)

# Set up authentication with your Spotify API credentials
client_id = "INSERT CLIENT ID HERE"
client_secret = "INSERT CLIENT SECRET HERE"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist = sp.playlist_items(playlist_uri)

offset = 0
counter = 0
with open("playlist.txt", "w") as f:
    while True:
        playlist = sp.playlist_items(playlist_uri, offset=offset)
        if len(playlist['items']) == 0:
            break
        for item in playlist['items']:
            track = item['track']
            artist_names = ", ".join([artist['name'] for artist in track['artists']])
            track_info = f"{track['name']} - {artist_names}\n"
            f.write(track_info)
            counter += 1
        offset += len(playlist['items'])

print(f"Total number of tracks: {counter}")

