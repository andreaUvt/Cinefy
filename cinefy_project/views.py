from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import openai
from django.contrib.auth.decorators import login_required
from django import views
from cinefy_app.models import Genre, Movie
from groq import Groq
from .utils import extract_groq_key



def Homepage(request):
    genres = Genre.objects.all()
    genre_movies = {genre.name: genre.movie_set.all()[:10] for genre in genres}
    tmdb_image_path = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"
    context = {
        'genre_movies': genre_movies,
        'tmdb_image_path': tmdb_image_path
    }
    return render(request, 'home.html')

def chatbot(request):
    if request.user.is_authenticated:
        username=request.user.username
        key=extract_groq_key("secrets.txt")
    if key is None:
        print("Groq api KEY ERROR. Check secrets.txt")
        quit()

    client = Groq(
        api_key=key
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello from now on I would like to talk to you about movies. My favorite genres are: comedy, horror and action. My favorite movie is Deadpool 3."
            }
        ],
        model="llama3-8b-8192",
    )
    chat_completion.choices[0].message.content
    return render(request,"chatbot.html",context={'username':username})

def getResponse(request):
    userMessage=request.GET.get('userMessage')

    key=extract_groq_key("secrets.txt")
    if key is None:
        print("Groq api KEY ERROR. Check secrets.txt")
        quit()

    client = Groq(
        api_key=key
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": userMessage
            }
        ],
        model="llama3-8b-8192",
    )

    response=chat_completion.choices[0].message.content

    return HttpResponse(response)