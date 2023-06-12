class Track:
    """"
    Track class
    """
    def __init__(self, track):
        self.album = track['album']
        self.artists = track['artists']
        self.available_markets = track['available_markets']
        self.disc_number = track['disc_number']
        self.duration_ms = track['duration_ms']
        self.explicit = track['explicit']
        self.external_ids = track['external_ids']
        self.external_urls = track['external_urls']
        self.href = track['href']
        self.id = track['id']
        self.is_local = track['is_local']
        self.name = track['name']
        self.popularity = track['popularity']
        self.preview_url = track['preview_url']
        self.track_number = track['track_number']
        self.type = track['type']
        self.uri = track['uri']
