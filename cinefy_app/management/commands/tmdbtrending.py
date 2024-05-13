from django.core.management.base import BaseCommand
from cinefy_app.utils import tmdbtrending

class Command(BaseCommand):
    help = 'Command for importing trending movies from tmdb.'

    def handle(self, *args, **options):
        tmdbtrending()
        self.stdout.write(self.style.SUCCESS('Trending movies imported!'))