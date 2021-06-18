import uuid

from django.db import models


class Pet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(default=0)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_pets(has_photos=None, offset=0, limit=20):
        if has_photos is None:
            pets = Pet.objects.prefetch_related('photos')[offset:offset + limit]
        elif has_photos:
            pets = Pet.objects.filter(photos__isnull=False).prefetch_related('photos')[offset:offset + limit]
        else:
            pets = Pet.objects.exclude(photos__isnull=False)[offset:offset + limit]
        return pets


class PetPhoto(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='')
