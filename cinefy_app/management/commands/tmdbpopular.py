from django.core.management.base import BaseCommand
from cinefy_app.utils import tmdbpopular

class Command(BaseCommand):
    help = 'Command for importing popular movies from tmdb.'

    def handle(self, *args, **options):
        tmdbpopular()
        self.stdout.write(self.style.SUCCESS('Popular movies imported!'))