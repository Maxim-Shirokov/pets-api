from rest_framework import serializers
from .models import Pet, PetPhoto


class PetAddPhotoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_image_url')
    file = serializers.ImageField(source='photo', write_only=True, use_url=True)

    class Meta:
        model = PetPhoto
        fields = ('id', 'file', 'url')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return PetPhoto.objects.create(**validated_data)

    def get_image_url(self, obj):
        return obj.photo.url


class PetSerializer(serializers.ModelSerializer):
    photos = PetAddPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = ('id', 'name', 'age', 'type', 'photos', 'created_at')

