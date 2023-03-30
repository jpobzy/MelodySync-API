class Playlist:
    def __init__(self, playlist):
        self.collaborative = playlist['collaborative']
        self.description = playlist['description']
        self.external_urls = playlist['external_urls']
        self.href = playlist['href']
        self.id = playlist['id']
        self.images = playlist['images']
        self.name = playlist['name']
        self.owner = playlist['owner']
        self.primary_color = playlist['primary_color']
        self.public = playlist['public']
        self.snapshot_id = playlist['snapshot_id']
        self.tracks = playlist['tracks']
        self.type = playlist['type']
        self.uri = playlist['uri']

    
    
    