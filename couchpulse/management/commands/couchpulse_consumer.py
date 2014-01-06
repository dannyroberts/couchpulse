from django.core import cache
from django.core.management import BaseCommand
from couchpulse import logreader


class Command(BaseCommand):
    def handle(self, *args, **options):
        logreader.consume_forever(cache=cache.get_cache('redis'))
