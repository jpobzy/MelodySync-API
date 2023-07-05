from src.item.artist import SimplifiedArtist

class Album:
    """
    Album class
    """
    def __init__(self, album):
        self.album_type = album['album_type']
        self.total_tracks = album['total_tracks']
        self.available_markets = album['available_markets']
        self.external_urls = album['external_urls']
        self.href = album['href']
        self.id = album['id']
        self.images = album['images']
        self.name = album['name']
        self.release_date = album['release_date']
        self.release_date_precision = album['release_date_precision']
        self.restrictions = album['restrictions'] if 'restrictions' in album and album['restrictions'] is not None else None
        self.type = album['type']
        self.uri = album['uri']
        self.copyrights = album['copyrights']
        self.external_ids = album['external_ids']
        self.genres = album['genres']
        self.label = album['label']
        self.popularity = album['popularity']
        self.artists = [SimplifiedArtist(artist) for artist in album['artists']] #album['artists']
        self.tracks = album['tracks']


           