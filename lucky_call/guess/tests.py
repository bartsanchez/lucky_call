from django import test

from guess import models
from guess import serializers


class GuessModelTests(test.TestCase):
    def test_valid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_id': 'fake_user_id',
            'keyword': 'fake_keyword',
            'number': 666,
            'timestamp': 1565460993,
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
            'timestamp': 1565460993,
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
            'timestamp': 1565460993,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertFalse(s.is_valid())
        self.assertIn('number', s.errors)
