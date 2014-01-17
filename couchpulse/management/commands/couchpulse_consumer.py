from django.core import cache
from django.core.management import BaseCommand
from raven.utils import json
from couchpulse import logreader


class Command(BaseCommand):
    def handle(self, *args, **options):
        if args:
            offsets = dict(enumerate(json.loads(args[0])))
        else:
            offsets = None

        logreader.consume_forever(cache=cache.get_cache('redis'), offsets=offsets)
