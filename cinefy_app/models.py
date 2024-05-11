from django.db import models
import uuid

# Create your models here.

class Genre(models.Model):
    id = models.IntegerField(unique=True, primary_key=True,editable=False)
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.id}: {self.name}"



class Movie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,editable=False)
    title = models.CharField(max_length=300,null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    vote_count = models.IntegerField(default=0,null=True,blank=True) 
    vote_average = models.FloatField(default=0,null=True,blank=True)
    tmdbvote_count = models.IntegerField(null=True,blank=True) 
    tmdbvote_average = models.FloatField(null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    runtime = models.IntegerField(null=True,blank=True)
    release_date = models.CharField(max_length=100, null=True, blank=True)
    poster_path = models.CharField(max_length=500, null=True, blank=True)
    popularity = models.CharField(max_length=100, null=True, blank=True)
    original_language = models.CharField(max_length=100, null=True, blank=True)
    origin_country = models.CharField(max_length=100, null=True, blank=True)
    tmdbid = models.CharField(max_length=100,null=True,blank=True)
    genres = models.ManyToManyField(Genre)
    adult = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.title)
    