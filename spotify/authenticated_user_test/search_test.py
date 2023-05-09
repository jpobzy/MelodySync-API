from playlist import search

class search_tests():
    def run_tests(spotifyAPI):
        search_object = search.Search(spotifyAPI)
        track_name = "Highlife"
        track_artist = "Logic"
        
        result = search_object.search_for_track(track_name=track_name, track_artist=track_artist)
        print(result)