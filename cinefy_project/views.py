from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import openai
from django.contrib.auth.decorators import login_required
from django import views
from cinefy_app.models import Genre, Movie
from cinefy_app.utils import tmdbtrending, tmdbpopular



def Homepage(request):
    genres = Genre.objects.all()
    genre_movies = {genre.name: genre.movie_set.all()[:10] for genre in genres}
    tmdb_image_path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context = {
        'genre_movies': genre_movies,
        'tmdb_image_path': tmdb_image_path
    }
    return render(request, 'home.html')


def get_completion(prompt): 
    print(prompt) 
    query = openai.Completion.create( 
        model="gpt-3.5-turbo-0125", 
        prompt=prompt, 
        max_tokens=100, 
        n=1, 
        stop=None, 
        temperature=0.5, 
    ) 
  
    response = query.choices[0].text 
    print("Response:", response) 
    return response 
  

@login_required(login_url='login')
def query_view(request): 
    
    if request.method == 'POST': 
        prompt = request.POST.get('prompt') 
        response = get_completion(prompt) 
        return JsonResponse({'response': response}) 
    
    return render(request, 'chatbot.html') 