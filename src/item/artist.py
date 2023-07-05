from src.item.response import new_response
from src.app.__innit__ import API

class Artist:
    """
    Artist class
    """
    def __init__(self, artist):
        self.external_url = artist['external_urls']
        self.followers = artist['followers']
        self.genres = artist['genres']
        self.href = artist['href']
        self.id = artist['id']
        self.image_url = artist['images'][0]['url'] if artist['images'] else None
        self.name = artist['name']
        self.popularity = artist['popularity']
        self.type = artist['type']
        self.uri = artist['uri']
        
        
class SimplifiedArtist:
    """
    SimplifiedArtist class 
    For album requests since it returns a simplified artist object
    """
    def __init__(self, artist):
        self.external_url = artist['external_urls']
        self.href = artist['href']
        self.id = artist['id']
        self.name = artist['name']
        self.type = artist['type']
        self.uri = artist['uri']
        
    def get_full_artist_details(self):
        """
        Returns the full details of an artist, Artist class
        """
        self.api = API()
        response = Artist(new_response.get(f'/artists/{self.id}', self.api.token))
        return response
    
    