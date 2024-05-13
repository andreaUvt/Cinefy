from .models import Genre,Movie
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
from django.db.models import Q

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def tmdbgenres():
    KEY="api_key="
    with open('secrets.txt', 'r') as file:
        for line in file:
            if line.startswith('TMDB_CLIENT_ID='):
                KEY+=( line[len('TMDB_CLIENT_ID='):].strip())
                break
        else:
            raise ValueError("TMDB_CLIENT_ID not found in secrets.txt")

    url = f"https://api.themoviedb.org/3/genre/movie/list?{KEY}"
    headers = {
        "accept": "application/json",
    }

    request = Request(url, headers=headers)
    response = urlopen(request)
            
    if response.getcode() != 200:
        print("API response error tmdb, not 200")
      
    data = json.loads(response.read().decode('utf-8'))

    for genre_data in data['genres']:
        genre_id = genre_data['id']
        genre_name = genre_data['name']
        print(genre_id,": ",genre_name)
        try:
            Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            Genre.objects.create(
                id=genre_id,
                name=genre_name,
                )
            
def saveMovie(data):
    movie_defaults = {
        'title': data.get('title', ''),
        'description': data.get('overview', ''),
        'tmdbvote_count': data.get('vote_count', 0),
        'tmdbvote_average': data.get('vote_average', 0),
        'status': data.get('status', ''),
        'runtime': data.get('runtime', None),
        'release_date': data.get('release_date', ''),
        'poster_path': data.get('poster_path', ''),
        'popularity': data.get('popularity', ''),
        'tmdbid': data.get('id', ''),
        'adult': data.get('adult', ''),
        'original_language': data.get('original_language', ''),
        'origin_country': ','.join(data.get('origin_country', [])), 
    }

    genres_data = data.get('genres', [])
    genres_data2= data.get('genre_ids',[])

    genres = []

    for genreID in genres_data:
        genreID = genres_data.get('id')
        genre = Genre.objects.get(id=genreID)
        genres.append(genre)

    for genreID in genres_data2:
        genre = Genre.objects.get(id=genreID)
        if genre not in genres:
            genres.append(genre)


    movie, created = Movie.objects.update_or_create(tmdbid=data.get('id'), defaults=movie_defaults)
    
    movie.genres.set(genres)
    movie.save()

    print(f"Movie saved - id: {data.get('id')}")

def tmdbtest():
    KEY="api_key="
    with open('secrets.txt', 'r') as file:
        for line in file:
            if line.startswith('TMDB_CLIENT_ID='):
                KEY+=( line[len('TMDB_CLIENT_ID='):].strip())
                break
        else:
            raise ValueError("TMDB_CLIENT_ID not found in secrets.txt")

    movie_id=293660
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?{KEY}"

    headers = {
        "accept": "application/json",
    }

    request = Request(url, headers=headers)
    response = urlopen(request)
            
    if response.getcode() != 200:
        print("API response error tmdb, not 200")
        quit()
          
    data = json.loads(response.read().decode('utf-8'))
    saveMovie(data)

def tmdbtrending():
    KEY="api_key="
    with open('secrets.txt', 'r') as file:
        for line in file:
            if line.startswith('TMDB_CLIENT_ID='):
                KEY+=( line[len('TMDB_CLIENT_ID='):].strip())
                break
        else:
            raise ValueError("TMDB_CLIENT_ID not found in secrets.txt")

    movie_id=293660
    url = f'https://api.themoviedb.org/3/trending/movie/day?{KEY}'

    headers = {
        "accept": "application/json",
    }

    request = Request(url, headers=headers)
    response = urlopen(request)
            
    if response.getcode() != 200:
        print("API response error tmdb, not 200")
        quit()
          
    data = json.loads(response.read().decode('utf-8'))
    for movie in data.get('results',[]):
        saveMovie(movie)

def searchMovie(request): # Search for podcasts by title
    search_movie = ""

    if request.GET.get('search_movie'):
        search_movie = request.GET.get('search_movie')

    allmovies= Movie.objects.filter(title__icontains=search_movie)
    return allmovies, search_movie

def paginateMovies(request, allmovies, results): # Paginator for podcasts

    page = request.GET.get('page')
    paginator = Paginator(allmovies, results)

    try:
        allmovies = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        allmovies = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        allmovies = paginator.page(page)

    leftIndex = (int(page) - 3)
    if leftIndex < 1:
        leftIndex = 1

    rigtIndex = (int(page) + 3)
    if rigtIndex > paginator.num_pages:
        rigtIndex=paginator.num_pages+1

    custom_range = range(leftIndex,rigtIndex)

    return custom_range, allmovies