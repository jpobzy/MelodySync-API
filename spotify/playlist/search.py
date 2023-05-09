class Search:
    def __init__(self, spotifyAPI):
        self.spotify = spotifyAPI.sp

    def search_for_track(self, track_name, track_artist):
        try:
            # Perform search query with track name and artist
            query = f'track:"{track_name}" artist:"{track_artist}"'
            results = self.spotify.search(q=query, type='track', limit=1)
            print(f"results is: {results}")

            # Extract track information from search results
            items = results.get('tracks', {}).get('items', [])
            if items:
                track = items[0]
                track_name = track['name']
                track_artist = track['artists'][0]['name']
                return {'track_name': track_name, 'track_artist': track_artist}
            else:
                print(f"No track found with name '{track_name}' and artist '{track_artist}'.")
                return None
        except Exception as e:
            print(f"Error searching for track: {str(e)}")
            return None


# TODO: implement these functions
    def search_for_tracks():
        pass

    def search_for_artist():
        pass

    def search_for_artists():
        pass

    def get_artist_albums():
        pass

    def get_artist_top_tracks():
        pass

