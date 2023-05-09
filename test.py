    def __init__(self, client_id, client_secret, redirect_uri, scope):
        sp_oauth  = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                        redirect_uri=redirect_uri, scope=scope)
