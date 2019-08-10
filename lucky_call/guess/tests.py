from django import test
from django.urls import reverse

from rest_framework import status

from guess import models
from guess import serializers


class GuessModelTests(test.TestCase):
    def test_valid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_id': 'fake_user_id',
            'keyword': 'fake_keyword',
            'number': 666,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertTrue(s.is_valid())

        s.save()

        self.assertEqual(models.Guess.objects.count(), 1)

    def test_invalid_guess_low(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_id': 'fake_user_id',
            'keyword': 'fake_keyword',
            'number': 99,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertFalse(s.is_valid())
        self.assertIn('number', s.errors)

    def test_invalid_guess_high(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_id': 'fake_user_id',
            'keyword': 'fake_keyword',
            'number': 1000,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertFalse(s.is_valid())
        self.assertIn('number', s.errors)


class MakeGuessViewTests(test.TestCase):
    def setUp(self):
        self.url = reverse('make-guess')

    def test_valid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)

        data = {
            'user_id': 'fake_user',
            'keyword': 'fake_keyword',
            'number': 888,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Guess.objects.count(), 1)

    def test_invalid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)

        data = {
            'user_id': 'fake_user',
            'keyword': 'fake_keyword',
            'number': 70,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Guess.objects.count(), 0)

    def test_incomplete_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)

        data = {
            'keyword': 'fake_keyword',
            'number': 486,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Guess.objects.count(), 0)

    def test_do_not_allow_multiple_guesses_per_user(self):
        data = {
            'user_id': 'fake_user',
            'keyword': 'fake_keyword',
            'number': 486,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Guess.objects.count(), 1)

        data = {
            'user_id': 'fake_user',
            'keyword': 'fake_keyword',
            'number': 123,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {'user_id': ['guess with this user id already exists.']}
        )
        self.assertEqual(models.Guess.objects.count(), 1)
