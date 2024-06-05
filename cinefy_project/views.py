from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import openai
from django.contrib.auth.decorators import login_required
from django import views
from cinefy_app.models import Genre, Movie
from groq import Groq
from .utils import extract_groq_key



def Homepage(request):

    # Presupunem că avem un model Genre și un model Movie deja definit

    # Obținerea obiectelor de genuri
    animatie = Genre.objects.get(name="Animation")
    actiune = Genre.objects.get(name="Action")
    aventura = Genre.objects.get(name="Adventure")
    comedie = Genre.objects.get(name="Comedy")
    drama = Genre.objects.get(name="Drama")
    fantasy = Genre.objects.get(name="Fantasy")
    horror = Genre.objects.get(name="Horror")
    mister = Genre.objects.get(name="Mystery")
    romantic = Genre.objects.get(name="Romance")
    sf = Genre.objects.get(name="Science Fiction")
    thriller = Genre.objects.get(name="Thriller")

    # Filtrarea filmelor după genuri
    filme_animatie = Movie.objects.filter(genres=animatie)
    filme_actiune = Movie.objects.filter(genres=actiune)
    filme_aventura = Movie.objects.filter(genres=aventura)
    filme_comedie = Movie.objects.filter(genres=comedie)
    filme_drama = Movie.objects.filter(genres=drama)
    filme_fantasy = Movie.objects.filter(genres=fantasy)
    filme_horror = Movie.objects.filter(genres=horror)
    filme_mister = Movie.objects.filter(genres=mister)
    filme_romantic = Movie.objects.filter(genres=romantic)
    filme_sf = Movie.objects.filter(genres=sf)
    filme_thriller = Movie.objects.filter(genres=thriller)

    tmdb_image_path="https://image.tmdb.org/t/p/w600_and_h900_bestv2"

    
    return render(request, 'home.html', {
    'filme_animatie': filme_animatie,
    'filme_actiune': filme_actiune,
    'filme_aventura': filme_aventura,
    'filme_comedie': filme_comedie,
    'filme_drama': filme_drama,
    'filme_fantasy': filme_fantasy,
    'filme_horror': filme_horror,
    'filme_mister': filme_mister,
    'filme_romantic': filme_romantic,
    'filme_sf': filme_sf,
    'filme_thriller': filme_thriller,
    'tmdb_image_path': tmdb_image_path
})

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
                "content": "Hello from now on I would like to talk to you about movies. I like thrillers, action and adventure. You can recommend me any kind of movies and movie genres, be creative and random about what you suggest."
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