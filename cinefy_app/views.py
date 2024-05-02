from django.shortcuts import render
from django import views

# Create your views here.
def moviesTEMP(request):
    return render(request, 'cinefy_app/movies.html')

def movieTEMP(request, pk):
    return render(request, 'cinefy_app/movie.html')