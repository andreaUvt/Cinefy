from django.shortcuts import render
from django import views
from .api import TMDBService
from django.contrib.auth.decorators import login_required
from .utils import searchMovie,paginateMovies
from .models import Movie,Genre,Watchlist,Watched
from django.http import HttpResponse

# Create your views here.
def movies(request):

    allmovies, search_movie=searchMovie(request)

    numberOfResultsPerPage=9
    custom_range, allmovies = paginateMovies(request,allmovies,numberOfResultsPerPage)
    tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context={'allmovies': allmovies, 'search_movie':search_movie, 'custom_range':custom_range, 'tmdb_image_path':tmdb_image_path}
    
    return render(request, 'cinefy_app/movies.html',context)

def movie(request, pk):
    if request.user.is_authenticated:
        profile = request.user.profile
        movie = Movie.objects.get(id=pk)
        if request.method == 'POST':
            action = request.POST['add_movie']
            if action == "+ Seen":
                if Watched.objects.filter(owner=profile, movie=movie).exists():
                    pass
                else:
                    toSave = Watched(owner=profile,movie=movie)
                    toSave.save()
                movie=Movie.objects.get(id=pk)
                tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
                context = {'movie':movie,'tmdb_image_path':tmdb_image_path}
                return render(request, 'cinefy_app/movie.html',context)
            elif action == "+ Watchlist":
                if Watchlist.objects.filter(owner=profile, movie=movie).exists():
                    pass
                else:
                    toSave = Watchlist(owner=profile,movie=movie)
                    toSave.save()
                movie=Movie.objects.get(id=pk)
                tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
                context = {'movie':movie,'tmdb_image_path':tmdb_image_path}
                return render(request, 'cinefy_app/movie.html',context)


        else:
            movie=Movie.objects.get(id=pk)
            tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
            context = {'movie':movie,'tmdb_image_path':tmdb_image_path}
            return render(request, 'cinefy_app/movie.html',context)

@login_required(login_url='login')
def watchlist(request):
    profile = request.user.profile
    movies_for_profile = Movie.objects.filter(watchlist__owner_id=profile.id)
    tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context = {'allmovies':movies_for_profile,'tmdb_image_path':tmdb_image_path}
    return render(request, 'cinefy_app/watchlist.html',context)

@login_required(login_url='login')
def watched(request):
    profile = request.user.profile
    movies_for_profile = Movie.objects.filter(watched__owner_id=profile.id)
    tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context = {'allmovies':movies_for_profile,'tmdb_image_path':tmdb_image_path}
    return render(request, 'cinefy_app/watchlist.html',context)
