from django.shortcuts import render,get_object_or_404,redirect
from django import views
from .api import TMDBService
from django.contrib.auth.decorators import login_required
from .utils import searchMovie,paginateMovies
from .models import Movie,Genre,Watchlist,Watched
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def movies(request):

    allmovies, search_movie=searchMovie(request)

    numberOfResultsPerPage=27
    custom_range, allmovies = paginateMovies(request,allmovies,numberOfResultsPerPage)
    tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context={'allmovies': allmovies, 'search_movie':search_movie, 'custom_range':custom_range, 'tmdb_image_path':tmdb_image_path}
    
    return render(request, 'cinefy_app/movies.html',context)


def movie(request, pk):
    if request.user.is_authenticated:
        profile = request.user.profile
        movie = Movie.objects.get(id=pk)
        if request.method == 'POST':
            action = request.POST.get('action') 
            if action == "+ Seen":
                if not Watched.objects.filter(owner=profile, movie=movie).exists():
                    Watched.objects.create(owner=profile, movie=movie)
                    messages.success(request,"Movie marked as seen")
                    Watchlist.objects.filter(owner=profile, movie=movie).delete()
            elif action == "+ Watchlist":
                if not Watchlist.objects.filter(owner=profile, movie=movie).exists():
                    Watchlist.objects.create(owner=profile, movie=movie)
                    messages.success(request,"Movie added to your watchlist")
                    
            elif action == "Delete":
                if not Watchlist.objects.filter(owner=profile, movie=movie).exists():
                    Watchlist.objects.delete(owner=profile,movie=movie)
                    print("Delete")

        tmdb_image_path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"
        context = {'movie': movie, 'tmdb_image_path': tmdb_image_path}
        return render(request, 'cinefy_app/movie.html', context)
    else:
        movie = get_object_or_404(Movie, id=pk)
        tmdb_image_path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"
        context = {'movie': movie, 'tmdb_image_path': tmdb_image_path}
        return render(request, 'cinefy_app/movie.html', context)

def delete_from_watchlist(request, pk):
    profile = request.user.profile
    movie = get_object_or_404(Movie, id=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "Delete":
            must_delete = Watchlist.objects.filter(owner=profile, movie=movie).first()
            if must_delete:
                must_delete.delete()
    return redirect('watchlist')
    

def delete_from_watched(request,pk):
    profile = request.user.profile
    movie= get_object_or_404(Movie,id=pk)
    if request.method== 'POST':
        action = request.POST.get('action')
        if action =="Delete":
            must_delete = Watched.objects.filter(owner=profile, movie=movie).first()
            if must_delete:
                must_delete.delete()
    return redirect('watched')


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
    return render(request, 'cinefy_app/watched.html',context)
