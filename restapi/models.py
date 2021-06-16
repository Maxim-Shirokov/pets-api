from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(default=0)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class PetPhoto(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='')
