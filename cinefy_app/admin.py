from django.contrib import admin

# Register your models here.
from .models import Movie,Genre,Watched,Watchlist

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Watchlist)
admin.site.register(Watched)