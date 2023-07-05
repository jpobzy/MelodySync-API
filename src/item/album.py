from src.item.artist import Artist, SimplifiedArtist

class Album:
    """
    Album class
    """
    
    def __init__(self, album):
        self.album_type = album['album_type']
        self.artists = [Artist(artist) for artist in album['artists']]
        self.available_markets = album['available_markets']
        self.copyrights = album['copyrights']
        self.external_ids = album['external_ids']
        self.external_urls = album['external_urls']
        self.genres = album['genres']
        self.href = album['href']
        self.id = album['id']
        self.images = album['images']
        self.label = album['label']
        self.name = album['name']
        self.popularity = album['popularity']
        self.release_date = album['release_date']
        self.release_date_precision = album['release_date_precision']
        self.restrictions = album['restrictions'] if 'restrictions' in album and album['restrictions'] is not None else None
        self.tracks = album['tracks']
        self.total_tracks = album['total_tracks']
        self.type = album['type']
        self.uri = album['uri']
        