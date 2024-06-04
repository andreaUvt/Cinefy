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

@login_required(login_url="login")
def chatbot(request):
    if not request.user.is_authenticated:
        return render(request, "chatbot.html")

    username = request.user.username
    key = extract_groq_key("secrets.txt")

    if key is None:
        print("Groq API KEY ERROR. Check secrets.txt")
        quit()

    if 'conversation_history' not in request.session:
        request.session['conversation_history'] = [
            {
                "role": "user",
                "content": "Hello from now on I would like to talk to you about movies. My favorite genres are: comedy, horror and action. My favorite movie is Deadpool 2."
            }
        ]

    return render(request, "chatbot.html", context={'username': username})

def getResponse(request):
    userMessage = request.GET.get('userMessage')
    key = extract_groq_key("secrets.txt")

    if key is None:
        print("Groq API KEY ERROR. Check secrets.txt")
        quit()

    client = Groq(api_key=key)

    conversation_history = request.session.get('conversation_history', [])
    conversation_history.append({"role": "user", "content": userMessage})

    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": response})

    request.session['conversation_history'] = conversation_history

    return HttpResponse(response)

def get_conversation_history(request):
    conversation_history = request.session.get('conversation_history', [])
    return JsonResponse(conversation_history, safe=False)