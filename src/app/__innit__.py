import json
import time
import requests
import os
from datetime import datetime
import webbrowser
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        auth_code = self.path.split('?')[1].split('=')[1]
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Authorization successful!</h1><p>You can now close this tab and return to the application.</p><script>window.close();</script></body></html>')
     
     
class API:
    def __init__(self):
        """
        Initializes creating the access/refresh tokens
        """
        if os.path.exists('.cache'):
            self.token_expired()
        else:   
            with open('config.json') as config_file:
                config = json.load(config_file)
            self.client_id = config['client_id']
            self.redirect_uri = config['redirect_uri']
            self.client_secret = config['client_secret']
            # self.auto_login = config['auto_login']
            
            
            with open('scopes/dev_scopes.json') as scopes_file:
                scopes = json.load(scopes_file)['scope']
                scope_string = ' '.join(scopes)
            self.scope = scope_string   
                
            server = HTTPServer(('localhost', 8080), CallbackHandler)
            authorization_base_url = 'https://accounts.spotify.com/authorize'
            params = {
                'client_id': self.client_id,
                'response_type': 'code',
                'redirect_uri':  self.redirect_uri,
                'scope': self.scope,
                # 'show_dialog' : self.auto_login
            }
            print(self.auto_login)
            authorization_url = authorization_base_url + '?' + urlencode(params)
            webbrowser.open_new_tab(authorization_url)
            server.timeout = 60  # Set the timeout to 60 seconds
            server.handle_request()
            authorization_code = auth_code
            token_url = 'https://accounts.spotify.com/api/token'
            data = {
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            response = requests.post(token_url, data=data)
            self.token = response.json()
            print(self.token)
            token_data = {
                'access_token': response.json()['access_token'],
                'refresh_token': response.json()['refresh_token'],
                'expires_at': int(time.time()) + response.json()['expires_in']
            }
            with open('.cache', 'w') as cache_file:
                json.dump(token_data, cache_file)               

    
    def create_refresh_token(self):
        refresh_token = None
        if os.path.exists('.cache'):
            print("DASDsad")
            with open('.cache') as cache_file:
                cache_data = json.load(cache_file)
                refresh_token = cache_data.get("refresh_token")
        
        with open('config.json') as config_file:
            config = json.load(config_file)
        self.client_id = config['client_id']
        self.redirect_uri = config['redirect_uri']
        self.client_secret = config['client_secret']
        with open('scopes/dev_scopes.json') as scopes_file:
            scopes = json.load(scopes_file)['scope']
            scope_string = ' '.join(scopes)
        self.scope = scope_string   
        if refresh_token:
            token_url = 'https://accounts.spotify.com/api/token'
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            response = requests.post(token_url, data=data)
            self.token = response.json()
            with open('.cache') as cache_file:
                cache_data = json.load(cache_file)
                cache_data['access_token'] = response.json()['access_token']
                cache_data['expires_at'] = int(time.time()) + response.json()['expires_in']
                with open('.cache', 'w') as rewrite:
                    json.dump(cache_data, rewrite)


    def token_expired(self):
        if not os.path.exists('.cache'):
            print('couldn\'t find .cache file, creating token')
            self.create_refresh_token()
        else:
            with open('.cache') as cache_file:
                cache_data = json.load(cache_file)
            expires_at = cache_data.get("expires_at")
            
            if expires_at is None or time.time() > expires_at:
                print("Token is expired")
                self.create_refresh_token()
                print("created refresh token")
            else:
                self.token = cache_data
                current_time = time.time()
                remaining_time = expires_at - current_time
                remaining_minutes = remaining_time // 60  # Divide by 60 to convert seconds to minutes
                remaining_seconds = remaining_time % 60
                remaining_time_str = f"{int(remaining_minutes)} minutes and {int(remaining_seconds)} seconds"
                expiry_time_str = datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S")
                print(f"Refresh token is not expired. Expires at: {expiry_time_str}. Time remaining: {remaining_time_str}")
            