import json
from distutils.util import strtobool

from restapi.serializers import PetSerializer
from django.core.management.base import BaseCommand
from restapi.models import Pet


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--has_photos', help='')

    def handle(self, *args, **options):
        has_photos = strtobool(options['has_photos']) if options['has_photos'] else None
        pets = Pet.get_pets(has_photos=has_photos)
        result = {'pets': []}
        for pet in pets:
            serializer = PetSerializer(pet).data
            photos = serializer['photos']
            serializer['photos'] = [photo['url'] for photo in photos if photo]
            result['pets'].append(serializer)

        self.stdout.write(json.dumps(result))
