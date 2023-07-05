from src.item.response import new_response
from src.app.__innit__ import API
import webbrowser

class Artist:
    """
    Artist class
    """
    def __init__(self, artist):
        self.external_url = artist['external_urls']
        self.followers = artist['followers'] if 'followers' in artist else None
        self.genres = artist['genres'] if 'genres' in artist else None
        self.href = artist['href']
        self.id = artist['id']
        self.image_url = artist['images'][0]['url']  if 'images' in artist else None #if artist['images'] else None
        self.name = artist['name']
        self.popularity = artist['popularity'] if 'popularity' in artist else None
        self.type = artist['type']
        self.uri = artist['uri']
        
        if not self.followers:
            self.get_full_artist_details()
        
    def get_full_artist_details(self):
        """
        Updates the instance with the full details of the artist
        """
        self.api = API()
        response = new_response.get(f'/artists/{self.id}', self.api.token)
        self.external_url = response['external_urls']
        self.followers = response['followers']
        self.genres = response['genres']
        self.image_url = response['images'][0]['url']
        self.popularity = response['popularity'] 
    
    