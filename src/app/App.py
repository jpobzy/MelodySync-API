from src.app.UserInfo import UserInfo
from src.app.MusicControls import MusicControls
from src.app.PlaylistOperations import PlaylistOperations
from src.app.DatabaseOperations import DatabaseOperations

class App(UserInfo, MusicControls, PlaylistOperations, DatabaseOperations):
    def __init__(self):
        UserInfo.__init__(self)
        MusicControls.__init__(self)
        PlaylistOperations.__init__(self)
        DatabaseOperations.__init__(self)