from django.core.management.base import BaseCommand
from cinefy_app.utils import watchproviders

class Command(BaseCommand):
    help = 'Command for importing currently available watch now link for Romania'

    def handle(self, *args, **options):
        watchproviders()
        self.stdout.write(self.style.SUCCESS('Watch provider link updated!'))