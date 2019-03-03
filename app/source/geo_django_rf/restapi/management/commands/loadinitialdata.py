from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Loads the geo-django-rf_restapi_initialdata fixture into the database'

    def handle(self, *args, **options):
        call_command('loaddata', 'geo-django-rf_restapi_initialdata.json')
