import requests
import json


class new_response:
    @staticmethod
    def code_handler(response):
        response.raise_for_status()
        if response.status_code == 204:
            print('response code was 204')
            return 204
        else:
            if response.content:  
                return response.json()
            else:
                return response
        
    @staticmethod
    def get(url, token, params=None, next="", json=None):
        """
        Url starts after https://api.spotify.com/v1
        """
        url = 'https://api.spotify.com/v1' + str(url)
        if next:
            url = ""
            url = next
        key = 'Bearer ' + token['access_token']
        headers = {'Authorization': key}
        response = requests.get(url=url, headers=headers, params=params, json=json)
        return new_response.code_handler(response)
        
        
    @staticmethod
    def post(url, token, application_json_headers_bool=False, data=None, json=None):
        """
        Url starts after https://api.spotify.com/v1
        """
        url = 'https://api.spotify.com/v1' + str(url)
        key = 'Bearer ' + token['access_token']
        headers = {'Authorization': key}
        if application_json_headers_bool:
            headers = headers = {'Authorization': key, 'Content-Type': 'application/json'}
        
        response = requests.post(url=url, headers=headers,json=json, data=data)
        return new_response.code_handler(response)
    
    @staticmethod
    def put(url, token, params=None, json=None):
        """
        Url starts after https://api.spotify.com/v1
        """
        url = 'https://api.spotify.com/v1' + str(url)
        key = 'Bearer ' + token['access_token']
        headers = {'Authorization': key}
        response = requests.put(url=url, headers=headers, params=params, json=json)
        return new_response.code_handler(response)

    @staticmethod
    def delete(url, token, params=None, json=None):
        """
        Url starts after https://api.spotify.com/v1
        """
        url = 'https://api.spotify.com/v1' + str(url)
        key = 'Bearer ' + token['access_token']
        headers = {'Authorization': key}
        response = requests.delete(url=url, headers=headers, params=params, json=json)
        return new_response.code_handler(response)
