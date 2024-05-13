from django.core.management.base import BaseCommand
from cinefy_app.utils import tmdbtest

class Command(BaseCommand):
    help = 'Command for importing a certain movie from tmdb.'

    def handle(self, *args, **options):
        tmdbtest()
        self.stdout.write(self.style.SUCCESS('Movie imported!'))