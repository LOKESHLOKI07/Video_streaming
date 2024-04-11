from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import ProductionLog

class ProductionLogTestCase(APITestCase):
    def setUp(self):
        self.username = 'umaa'
        self.password = 'davincicode3'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = APIClient()

    def test_production_log_api(self):
        # Authenticate the client using the user's credentials
        self.client.login(username=self.username, password=self.password)

        # Access the production-log-list endpoint
        url = reverse('production-log-list')
        response = self.client.get(url)

        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class VideoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_video_list_api(self):
        response = self.client.get(reverse('video-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_detail_api(self):
        response = self.client.get(reverse('video-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_video_search(self):
        response = self.client.get(reverse('video-search') + '?query=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_create(self):
        response = self.client.post(reverse('video-create'), {'title': 'Test Video', 'description': 'Test Description'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_video_update(self):
        response = self.client.post(reverse('video-update', args=[1]), {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_video_delete(self):
        response = self.client.post(reverse('video-delete', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class ProductionLogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_production_log_list_api(self):
        response = self.client.get(reverse('production-log-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_production_log_create(self):
        response = self.client.post(reverse('production-log-create'),
                                    {'cycle_no': '1', 'unique_id': '123', 'material_name': 'Test Material'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_production_log_update(self):
        response = self.client.post(reverse('production-log-update', args=[1]), {'cycle_no': '2'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_production_log_delete(self):
        response = self.client.post(reverse('production-log-delete', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
