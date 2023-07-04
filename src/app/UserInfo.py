from .__innit__ import API
from src.item.response import new_response
import webbrowser

class UserInfo:
    def __init__(self):
        self.api = API()
        
    def user_info(self):
        """
        Returns all information about current user
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)
    
    def user_country(self):
        """
        Returns the country of the user, as set in the user's account profile
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['country']        
    
    def user_display_name(self):
        """
        Returns current authenticated user's display name
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['display_name']

    def user_email(self):
        """
        Returns current users email
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['email']


    def user_explicit_content(self):
        """
        Returns current users explicit content settings
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['explicit_content']
    
    def user_external_urls(self):
        """
        Returns current users known urls
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['external_urls']


    def user_followers_count(self):
        """
        Returns current users follower count
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['followers']['total']
    
    def user_href(self):
        """
        Returns current users link to the Web API endpoint
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['href']
    
    def user_id(self):
        """
        Returns current authenticated user's ID
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['id']
    
    def user_subscription_level(self):
        """
        Returns users Spotify subscription level
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['product']
    
    
    def user_profile_image_url(self):
        """"
        Returns and opens users profile image url in webbrowser
        """
        self.api.token_expired()
        url = new_response.get('/me',self.api.token)['images'][-1]['url']
        webbrowser.open(url)
        return url
    
    def user_uri(self):
        """"
        Returns current authenticated user's uri
        """
        self.api.token_expired()
        return new_response.get('/me', self.api.token)['uri']
    
