
from src.app.UserInfo import UserInfo
from src.item.response import new_response
from src.item.playlist import Playlist
from src.item.track import Track
from src.app.UserInfo import UserInfo
from src.app.SearchOperations import Search_operations
from src.app.PlaylistOperations import PlaylistOperations
import time
from datetime import datetime
from src.app.DatabaseOperations import DatabaseOperations
import os
import random

class PlaylistGenerator:
    def __init__(self, api) :
        self.api = api
        
    def get_available_genre_seeds(self):
        return new_response.get('/recommendations/available-genre-seeds',self.api.token)
    
    
    def main(self, track_amount, seed_artists, seed_genres, seed_tracks, country='US'):
        params = {
           'limit': track_amount, 
            'market' : country,
            'seed_artists': seed_artists, 
            'seed_genres' : seed_genres,
            'seed_tracks' : seed_tracks
            }
        response = new_response.get('/recommendations',self.api.token, params=params)
        return response
    
    
    def read_and_grab_seeds(self):
        max_lines = 5 
        artists_seeds_arr = []
        tracks_seeds_arr = []
        
        def validate_lines(lines):
            if len(lines) > max_lines:
                raise ValueError(f"More than {max_lines} lines populated in the seed file")

        with open('./src/seeds/ArtistSeeds.txt', 'r') as artist_seeds:
            artists = [line.strip() for line in artist_seeds if line.strip()]
            validate_lines(artists)
            
        for artist in artists:
            artists_seeds_arr.append(Search_operations(self.api).search_for_artist(artist).id)          
            
        with open('./src/seeds/GenreSeeds.txt', 'r') as genre_seeds:
            genres = [line.strip() for line in genre_seeds if line.strip()]
            validate_lines(genres)
            
        for genre in genres:
            if genre not in self.get_available_genre_seeds()['genres']:
                raise ValueError('Invalid genre given')            

        with open('./src/seeds/TrackSeeds.txt', 'r') as track_seeds:
            tracks = [line.strip() for line in track_seeds if line.strip()]
            validate_lines(tracks)

        for track in tracks: 
            tracks_seeds_arr.append(Search_operations(self.api).search_for_track(track).id)

        if len(artists_seeds_arr) + len(genres) + len(tracks_seeds_arr) > 5:
            raise ValueError(f"More than 5 seeds were given in total")
        
        artists = ','.join(artists_seeds_arr)
        genres = ','.join(genres)
        tracks = ','.join(tracks_seeds_arr)
        return (artists, genres, tracks)

    
    def generate_playlist(self, track_amount):
        generate_seed_ids = self.read_and_grab_seeds()
        seed_artists = generate_seed_ids[0]
        seed_genres = generate_seed_ids[1]
        seed_tracks = generate_seed_ids[2]
        response = self.main(track_amount, seed_artists, seed_genres, seed_tracks) 
        playlist_name = f'Generated Playlist {str(random.randint(0, 1000))}'
        creation_time = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        new_playlist = PlaylistOperations(self.api).create_playlist(playlist_name, f'Created at {creation_time}')
        song_uri_list = [tracks['uri'] for tracks in response['tracks']]
        PlaylistOperations(self.api).add_songs_to_playlist(playlist_id=new_playlist['id'], song_uri_list=song_uri_list)
        db = DatabaseOperations(self.api)
        new_db = db.create_generated_playlist_library()
        db.add_playlist_to_generated_playlist_library(response,  new_db, playlist_name, track_amount)

            