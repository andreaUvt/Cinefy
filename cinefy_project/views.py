from django.shortcuts import render
from django import views

def Homepage(request):
    return render(request, 'home.html')