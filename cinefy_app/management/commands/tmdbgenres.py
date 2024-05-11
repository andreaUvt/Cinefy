from django.core.management.base import BaseCommand
from cinefy_app.utils import tmdbgenres

class Command(BaseCommand):
    help = 'Command for importing currently available genres from tmdb api service.'

    def handle(self, *args, **options):
        tmdbgenres()
        self.stdout.write(self.style.SUCCESS('Genres imported!'))