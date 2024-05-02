# tmdb_service.py

import requests

class TMDBService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3/'

    def search_movies(self, query):
        url = f"{self.base_url}search/movie"
        params = {'api_key': self.api_key, 'query': query}
        response = requests.get(url, params=params)
        return response.json()

    def get_movie_details(self, movie_id):
        url = f"{self.base_url}movie/{movie_id}"
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params)
        return response.json()
