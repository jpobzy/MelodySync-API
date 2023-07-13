from src.app.UserInfo import UserInfo
from src.app.MusicControls import MusicControls
from src.app.PlaylistOperations import PlaylistOperations
from src.app.DatabaseOperations import DatabaseOperations
from src.app.AlbumOperations import AlbumOperations
from src.app.ArtistOperations import ArtistOperations
from src.app.SearchOperations import Search_operations
from src.app.__innit__ import API
from src.app.PlaylistGenerator import PlaylistGenerator
from src.item.album import Album

class App(PlaylistGenerator, Album, Search_operations,UserInfo, MusicControls, PlaylistOperations, DatabaseOperations, AlbumOperations, ArtistOperations):
    def __init__(self):
        api = API()
        UserInfo.__init__(self, api)
        MusicControls.__init__(self, api)
        PlaylistOperations.__init__(self, api)
        DatabaseOperations.__init__(self, api)
        Search_operations.__init__(self, api)
        PlaylistGenerator.__init__(self, api)
        # Search_operations.__init__(self, api)
        
        # AlbumOperations.__init__(self, api)
        # ArtistOperations.__init__(self, api)