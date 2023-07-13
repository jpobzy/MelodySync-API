from src.item.response import new_response
from src.item.track import Track
from src.item.artist import Artist
from src.item.album import Album
from src.item.playlist import Playlist
from urllib.parse import quote
from thefuzz import fuzz

class Search_operations:
    
    def __init__(self, api):
        self.api = api

    def search_for_album(self, album_name, track_artist = "", limit=1, offset=0, return_idx=-1):
        search_query = f"remaster%20album:{quote(album_name.replace(' ', ''))}"
        params = {
            "q": search_query,
            "type": ["album"],
            'limit': limit,
            'offset': offset
        }
        if track_artist:
            params["q"] += f"%20artist:{track_artist.replace(' ', '')}"
        respo = new_response.get("/search", self.api.token, params=params)  

        return Album(respo['albums']['items'][return_idx])


    def search_for_artist(self, artist_name, market='US', genre=None, limit=20, offset=0, return_idx=-1):
        query_params = {
            "q": artist_name,
            "type": "artist",
            'market': market,
            'limit': limit,
            'offset': offset
        }
        if genre:
            query_params["genre"] = genre
        respo = new_response.get("/search", self.api.token, params=query_params)
        query = artist_name
        query_lower = query.lower()
        matched_artists = []
        for artist in respo['artists']['items']:
            artist_name = artist['name'].lower()
            similarity_ratio = fuzz.ratio(query_lower, artist_name)
            if similarity_ratio > 70:  # Set an appropriate threshold for similarity
                matched_artists.append((artist['name'], similarity_ratio, artist['popularity'], artist))

        if matched_artists:
            matched_artists.sort(key=lambda x: x[2], reverse=True)
            artist_name, similarity, popularity, artist = matched_artists[0]  # Get the most popular artist
            # print(f"Artist: {artist_name} (Similarity: {similarity}, Popularity: {popularity})")
            return Artist(artist)
        else:
            raise ValueError("No matching artists found.")

        

    def search_for_track(self, track_name, track_artist = "", limit=1, offset=0, return_idx=-1 ):
        """
        Returns Simplified Track
        0 < limit < 50
        0 < offset < 1000
        return_idx <= limit
        """
        params = {
            "q": f"remaster%20track:{track_name}",
            "type": ["track"],
            'limit': limit,
            'offset': offset
        }
        if track_artist:
            params["q"] += f"%20artist:{track_artist}"
        respo = new_response.get("/search", self.api.token, params=params)
        # print(f'Returning Track: {respo["tracks"]["items"][-1]["name"]}')
        return Track(respo['tracks']['items'][return_idx])    
        
                
            
