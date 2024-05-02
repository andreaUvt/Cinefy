from django.urls import path
from . import views

urlpatterns = [
    path('movie/<str:pk>/', views.movieTEMP, name="movie"),
    path('movies/', views.moviesTEMP, name="movies"),
]