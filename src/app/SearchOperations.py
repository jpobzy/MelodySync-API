from src.item.response import new_response
from src.item.track import Track
from src.item.artist import Artist
from src.item.album import Album
from src.item.playlist import Playlist
from urllib.parse import quote

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


    def search_for_artist(self, artist_name, limit=1, offset=0, return_idx=-1):
        search_query = f"remaster%20artist:{quote(artist_name.replace(' ', ''))}"
        query_params = {
            "q": search_query,
            "type": "artist",
            'limit': limit,
            'offset': offset
        }
        respo = new_response.get("/search", self.api.token, params=query_params)
        return Artist(respo['artists']['items'][return_idx])
        

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
        return Track(respo['tracks']['items'][return_idx])    

   

            
            
            
