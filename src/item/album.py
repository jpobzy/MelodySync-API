from src.item.artist import Artist
from src.app.__innit__ import API
from src.item.response import new_response

class Album:
    """
    Album class
    """
    
    def __init__(self, album):
        self.album_type = album['album_type'] 
        self.artists = [Artist(artist) for artist in album['artists']]
        self.available_markets = album['available_markets']
        self.copyrights = album['copyrights'] if 'copyrigts' in album else None
        self.external_ids = album['external_ids'] if 'external_ids' in album else None
        self.external_urls = album['external_urls']
        self.genres = album['genres'] if 'genres' in album else None
        self.href = album['href']
        self.id = album['id']
        self.images = album['images']
        self.label = album['label'] if 'label' in album else None
        self.name = album['name']
        self.popularity = album['popularity'] if 'popularity' in album else None
        self.release_date = album['release_date']
        self.release_date_precision = album['release_date_precision']
        self.restrictions = album['restrictions'] if 'restrictions' in album and album['restrictions'] is not None else None
        self.tracks = album['tracks'] if 'tracks' in album else None
        self.total_tracks = album['total_tracks']
        self.type = album['type']
        self.uri = album['uri']
        
        
    def get_full_album_details(self):
        """
        Updates the instance with the full details of the album
        """
        self.api = API()
        response = new_response.get(f'/albums/{self.id}', self.api.token)
        self.copyrights = response['copyrights']
        self.external_ids = response['external_ids']
        self.genres = response['genres']
        self.label = response['label']
        self.popularity = response['popularity']
        self.restrictions = response['restrictions']
        self.tracks = response['tracks']
