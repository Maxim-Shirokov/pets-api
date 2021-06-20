import shutil
import uuid
from unittest import mock

from pet import settings
from django.test import TestCase, Client, override_settings, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from restapi.serializers import PetSerializer
from restapi.models import Pet, PetPhoto


@override_settings(API_KEY=None)
class DefaultSetUp(TestCase):
    client = Client()
    ids = [uuid.uuid4() for _ in range(3)]

    def setUp(self):
        Pet.objects.create(
            id=self.ids[0],
            name="first",
            age=1,
            type="dog",
        )
        Pet.objects.create(
            id=self.ids[1],
            name="second",
            age=2,
            type="cat",
        )
        Pet.objects.create(
            id=self.ids[2],
            name="third",
            age=3,
            type="cat",
        )
        PetPhoto.objects.create(
            pet_id=self.ids[0],
            photo=mock.MagicMock(name='', spec=SimpleUploadedFile)
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT + '/MagicMock', ignore_errors=True)
        super().tearDownClass()


class GetPetsTest(DefaultSetUp):
    request = RequestFactory()

    def test_get_all_pets(self):
        url = '/pets'
        response = self.client.get(url)
        pets = Pet.objects.all()
        serializer = self.get_serializer(pets, url)
        self.assertEqual(response.data['item'], serializer.data)
        self.assertEqual(response.data['count'], pets.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_limit(self):
        response = self.client.get('/pets?limit=-1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invalid_offset(self):
        response = self.client.get('/pets?offset=-1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_with_limit_pets(self):
        url = '/pets?limit=2'
        response = self.client.get(url)
        pets = Pet.objects.all()[:2]
        serializer = self.get_serializer(pets, url)
        self.assertEqual(response.data['item'], serializer.data)
        self.assertEqual(response.data['count'], pets.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_with_offset_pets(self):
        url = '/pets?offset=1'
        response = self.client.get(url)
        pets = Pet.objects.all()[1:]
        serializer = self.get_serializer(pets, url)
        self.assertEqual(response.data['item'], serializer.data)
        self.assertEqual(response.data['count'], pets.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_with_has_photo(self):
        url = '/pets?has_photos=True'
        response = self.client.get(url)
        pets = Pet.objects.filter(photos__isnull=False)
        serializer = self.get_serializer(pets, url)
        self.assertEqual(response.data['item'], serializer.data)
        self.assertEqual(response.data['count'], pets.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url1 = '/pets?has_photos=False'
        response = self.client.get(url1)
        pets = Pet.objects.exclude(photos__isnull=False)
        serializer = self.get_serializer(pets, url1)
        self.assertEqual(response.data['item'], serializer.data)
        self.assertEqual(response.data['count'], pets.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_serializer(self, pets, url):
        return PetSerializer(pets, many=True, context={'request': self.request.get(url)})


class DeletePetsTest(DefaultSetUp):

    def test_delete_all(self):
        response = self.client.delete('/pets', data={'ids': self.ids}, content_type='application/json')
        self.assertEqual(response.data['deleted'], len(self.ids))
        self.assertEqual(response.data['errors'], [])

    def test_delete_with_error(self):
        other_uuid = uuid.uuid4()
        ids = [self.ids[0], other_uuid]
        response = self.client.delete('/pets', data={'ids': ids}, content_type='application/json')
        self.assertEqual(response.data['deleted'], 1)
        self.assertEqual(str(other_uuid), response.data['errors'][0]['id'])


class PostPetsPhotoTest(DefaultSetUp):

    def test_post_invalid_id(self):
        photo = mock.MagicMock(name='', spec=SimpleUploadedFile)
        response = self.client.post('/pets/1/photo', data={'file': photo}, content_type='form data')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_photo(self):
        response = self.client.post(f'/pets/{self.ids[0]}/photo')

