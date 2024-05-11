from .models import Genre,Movie
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json

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
    if 'title' in data:
        title=data['title']
    if 'overview' in data:
        description=data['overview']
    if 'vote_count' in data:
        tmdbvote_count=data['vote_count']
    if 'vote_average' in data:
        tmdbvote_average=data['vote_average']
    if 'status' in data:
        status=data['status']
    if 'runtime' in data:
        runtime=data['runtime']
    if 'release_date' in data:
        release_date=data['release_date']
    if 'poster_path' in data:
        poster_path=data['poster_path']
    if 'popularity' in data:
        popularity=data['popularity']
    if 'id' in data:
        tmdbid=data['id']
    if 'adult' in data:
        adult=data['adult']
    if 'original_language' in data:
        original_language=data['original_language']
    origin_country=""
    if 'origin_country':
        for country in data['origin_country']:
            origin_country += country
            origin_country+=","
 
    try:
        Movie.objects.get(tmdbid=data['id'])
    except Genre.DoesNotExist:
        Genre.objects.create(
            ...
            )