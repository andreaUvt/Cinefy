from django.shortcuts import render
from django import views
from .api import TMDBService

# Create your views here.
def moviesTEMP(request):
    return render(request, 'cinefy_app/movies.html')

def movieTEMP(request, pk):
    return render(request, 'cinefy_app/movie.html')

def search_movies(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        tmdb_service = TMDBService(api_key='65546db5f400f8a4de0d1776bf8e179a')
        search_results = tmdb_service.search_movies(query)
        return render(request, 'search_results.html', {'search_results': search_results})
    return render(request, 'search.html')

def movie_details(request, movie_id):
    tmdb_service = TMDBService(api_key='65546db5f400f8a4de0d1776bf8e179a')
    movie_details = tmdb_service.get_movie_details(movie_id)
    return render(request, 'movie_details.html', {'movie_details': movie_details})