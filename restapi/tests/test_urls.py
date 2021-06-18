from django.test import TestCase, Client, override_settings

from rest_framework import status


@override_settings(API_KEY='1')
class HeaderTest(TestCase):
    client = Client()

    def test_get_with_bad_header(self):
        response = self.client.get('/pets', HTTP_X_API_KEY='2')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_with_bad_header(self):
        response = self.client.post('/pets', HTTP_X_API_KEY='2')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_with_bad_header(self):
        response = self.client.delete('/pets', HTTP_X_API_KEY='2')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_photo_with_bad_header(self):
        response = self.client.post('/pets/1/photo', HTTP_X_API_KEY='2')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_with_good_header(self):
        response = self.client.get('/pets', HTTP_X_API_KEY='1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_with_good_header(self):
        """Должен возвращать 400, т.к не были переданы обязательные параметры: name, type"""
        response = self.client.post('/pets', HTTP_X_API_KEY='1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_with_good_header(self):
        response = self.client.delete('/pets', HTTP_X_API_KEY='1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_photo_with_good_header(self):
        """Должен возвращать 400, т.к id=1 некорретный uuid"""
        response = self.client.post('/pets/1/photo', HTTP_X_API_KEY='1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

