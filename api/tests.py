from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profissional

class ProfissionalTests(APITestCase):
    def test_criar_profissional(self):
        url = reverse('profissional-list')
        data = {'nome_social': 'Dr. House', 'profissao': 'infectologista', 'endereco': 'Rua do house, 123', 'contato': '123456789'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profissional.objects.count(), 1)
        self.assertEqual(Profissional.objects.get().nome_social, 'Dr. House')