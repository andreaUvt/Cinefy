from django.urls import path
from . import views

urlpatterns = [
    path('movie/<str:pk>/', views.movie, name="movie"),
    path('movies/', views.movies, name="movies"),
    path('watchlist/', views.watchlist, name="watchlist"),
    path('watched/', views.watched, name="watched"),
]