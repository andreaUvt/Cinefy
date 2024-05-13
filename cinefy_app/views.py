from django.shortcuts import render
from django import views
from .api import TMDBService
from django.contrib.auth.decorators import login_required
from .utils import searchMovie,paginateMovies
from .models import Movie,Genre

# Create your views here.
def movies(request):

    allmovies, search_movie=searchMovie(request)

    numberOfResultsPerPage=9
    custom_range, allmovies = paginateMovies(request,allmovies,numberOfResultsPerPage)
    tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context={'allmovies': allmovies, 'search_movie':search_movie, 'custom_range':custom_range, 'tmdb_image_path':tmdb_image_path}
    
    return render(request, 'cinefy_app/movies.html',context)

def movie(request, pk):
    movie=Movie.objects.get(id=pk)
    tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context = {'movie':movie,'tmdb_image_path':tmdb_image_path}
    return render(request, 'cinefy_app/movie.html',context)

@login_required(login_url='login')
def watchlist(request):
    return render(request, 'cinefy_app/watchlist.html')

@login_required(login_url='login')
def watched(request):
    return render(request, 'cinefy_app/watched.html')
