from src.item.artist import Artist

class Track:
    """
    Track class
    """
    def __init__(self, track):
        self.album = track['album'] 
        self.artists = [Artist(artist) for artist in track['artists']] 
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

    def get_artists_names(self):
        num_artists = len(self.artists)
        if num_artists == 1:
            return self.artists[0].name
        elif num_artists == 2:
            return self.artists[0].name + ' and ' + self.artists[1].name
        elif num_artists > 2:
            artists = [artist.name for artist in self.artists]
            return ', '.join(artists[:-1]) + ', and ' + artists[-1]
            
        
    # def get_full_track_details(self, track):
    #     self.album = track['album'] if 'album' in track else None
    #     self.artists = [Artist(artist) for artist in track['artists']] if 'artists' in track else None
    #     self.available_markets = track['available_markets'] if 'available_markets' in track else None
    #     self.disc_number = track['disc_number'] if 'disc_number' in track else None
    #     self.duration_ms = track['duration_ms'] if 'duration_ms' in track else None
    #     self.explicit = track['explicit'] if 'explicit' in track else None
    #     self.external_ids = track['external_ids'] if 'external_ids' in track else None
    #     self.external_urls = track['external_urls'] if 'external_urls' in track else None
    #     self.href = track['href'] if 'href' in track else None
    #     self.id = track['id'] if 'id' in track else None
    #     self.is_local = track['is_local'] if 'is_local' in track else None
    #     self.name = track['name'] if 'name' in track else None
    #     self.popularity = track['popularity'] if 'popularity' in track else None
    #     self.preview_url = track['preview_url'] if 'preview_url' in track else None
    #     self.track_number = track['track_number'] if 'track_number' in track else None
    #     self.type = track['type'] if 'type' in track else None
    #     self.uri = track['uri'] if 'uri' in track else None