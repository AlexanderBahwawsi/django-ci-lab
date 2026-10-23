from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Dog


class DogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dog_data = {'name': 'Fido', 'breed': 'Labrador', 'age': 3}
        self.response = self.client.post('/dogs/', self.dog_data, format='json')

    def test_create_dog(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(Dog.objects.get().name, 'Fido')

    def test_get_dog(self):
        dog = Dog.objects.get()
        response = self.client.get(f'/dogs/{dog.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], dog.name)

    def test_update_dog(self):
        dog = Dog.objects.get()
        updated = {'name': 'Fido', 'breed': 'Labrador', 'age': 4}
        response = self.client.put(f'/dogs/{dog.id}/', updated, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Dog.objects.get().age, 4)

    def test_delete_dog(self):
        dog = Dog.objects.get()
        response = self.client.delete(f'/dogs/{dog.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dog.objects.count(), 0)
