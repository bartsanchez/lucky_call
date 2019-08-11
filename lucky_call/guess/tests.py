from django import test
from django.urls import reverse

from rest_framework import status

from guess import models
from guess import serializers


class GuessModelTests(test.TestCase):
    def test_valid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_email': 'test@example.com',
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
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 99,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertFalse(s.is_valid())
        self.assertIn('number', s.errors)

    def test_invalid_guess_high(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_email': 'test@example.com',
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
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 888,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Guess.objects.count(), 1)

    def test_invalid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)

        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 70,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Guess.objects.count(), 0)

    def test_incomplete_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)

        data = {
            'user_email': 'test@example.com',
            'number': 486,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Guess.objects.count(), 0)

    def test_do_not_allow_multiple_guesses_per_user(self):
        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 486,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Guess.objects.count(), 1)

        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 123,
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {'user_email': ['guess with this user email already exists.']})
        self.assertEqual(models.Guess.objects.count(), 1)


class ContestGuessRelantionshipTest(test.TestCase):
    def test_no_contest_exist(self):
        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 666,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(models.Guess.objects.count(), 1)

        guess = models.Guess.objects.first()
        self.assertIsNone(guess.contest)

    def test_a_contest_exist(self):
        contest = models.LuckyCallContest.objects.create(
            keyword='fake_keyword',
        )
        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 666,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(models.Guess.objects.count(), 1)

        guess = models.Guess.objects.first()
        self.assertEqual(guess.contest, contest)

    def test_a_new_contest_start(self):
        contest = models.LuckyCallContest.objects.create(
            keyword='fake_keyword',
        )
        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 666,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(models.Guess.objects.count(), 1)

        guess = models.Guess.objects.first()
        self.assertEqual(guess.contest, contest)

        new_contest = models.LuckyCallContest.objects.create(
            keyword='another_keyword',
        )
        data = {
            'user_email': 'foo@bar.baz',
            'keyword': 'another_keyword',
            'number': 777,
        }
        s = serializers.GuessSerializer(data=data)

        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(models.Guess.objects.count(), 2)

        new_guess = models.Guess.objects.get(user_email='foo@bar.baz')
        self.assertEqual(new_guess.contest, new_contest)
