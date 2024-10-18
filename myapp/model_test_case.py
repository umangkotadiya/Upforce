from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Post

class BlogTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_account(self):
        url = reverse('create_account')
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'newuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_blog(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('create_blog')
        data = {'title': 'Test Blog', 'description': 'Test Description', 'content': 'Test Content', 'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
