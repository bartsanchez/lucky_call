import datetime

from django import test
from django.urls import reverse

from rest_framework import status

from guess import factories
from guess import models
from guess import serializers
from guess import tasks


class GuessModelTests(test.TestCase):
    def test_representation(self):
        guess = factories.GuessFactory(user_email='fake@email.com')
        self.assertIn('fake@email.com', repr(guess))

    def test_valid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 666,
            'timestamp': datetime.datetime.now(),
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
            'timestamp': datetime.datetime.now(),
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
            'timestamp': datetime.datetime.now(),
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

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
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

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
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
            {'errors': ['Invalid request.']})
        self.assertEqual(models.Guess.objects.count(), 1)


class ContestGuessRelantionshipTest(test.TestCase):
    def test_no_contest_exist(self):
        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 666,
            'timestamp': datetime.datetime.now(),
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
            'timestamp': datetime.datetime.now(),
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
            'timestamp': datetime.datetime.now(),
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
            'timestamp': datetime.datetime.now(),
        }
        s = serializers.GuessSerializer(data=data)

        self.assertTrue(s.is_valid())
        s.save()

        self.assertEqual(models.Guess.objects.count(), 2)

        new_guess = models.Guess.objects.get(user_email='foo@bar.baz')
        self.assertEqual(new_guess.contest, new_contest)


class LucyContestModelTests(test.TestCase):
    def test_guesses(self):
        contest = factories.LuckyCallContestFactory(keyword='foo')

        guess_1 = factories.GuessFactory(
            user_email='user1@example.com',
            keyword='foo',
            number=111,
        )
        guess_2 = factories.GuessFactory(
            user_email='user2@example.com',
            keyword='foo',
            number=222,
        )

        self.assertQuerysetEqual(
            contest.guesses,
            models.Guess.objects.filter(pk__in=(guess_1.pk, guess_2.pk)),
            ordered=False,
            transform=lambda x: x
        )

    def test_is_winner(self):
        contest = factories.LuckyCallContestFactory(result=1364)

        self.assertTrue(contest.is_winner())

    def test_is_not_winner(self):
        contest = factories.LuckyCallContestFactory(result=999)

        self.assertFalse(contest.is_winner())

    def test_we_have_already_a_winner(self):
        guess = factories.GuessFactory(
            user_email='user1@example.com',
            keyword='foo',
            number=111,
        )
        contest = factories.LuckyCallContestFactory(
            keyword='foo',
            winner=guess,
        )

        self.assertEqual(contest.check_winner(), guess)


class ExampleWinnerScenario(test.TestCase):
    def test_someone_won(self):
        contest = factories.LuckyCallContestFactory(keyword='foo')

        factories.GuessFactory(
            user_email='user1@example.com',
            keyword='foo',
            number=111,
        )
        factories.GuessFactory(
            user_email='user2@example.com',
            keyword='foo',
            number=222,
        )

        contest = models.LuckyCallContest.objects.get(pk=contest.pk)

        self.assertIsNone(contest.check_winner())
        self.assertEqual(contest.result, 333)
        self.assertIsNone(contest.winner)

        guess = factories.GuessFactory(
            user_email='user3@example.com',
            keyword='foo',
            number=107,
        )

        self.assertEqual(contest.check_winner(), guess)
        self.assertEqual(contest.result, 440)
        self.assertEqual(contest.winner, guess)


class CreateGuessTaskTests(test.TestCase):
    def test_valid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'user_email': 'test@example.com',
            'keyword': 'fake_keyword',
            'number': 666,
            'timestamp': datetime.datetime.now(),
        }
        self.assertEqual(tasks.create_guess(data=data), 'OK')

        self.assertEqual(models.Guess.objects.count(), 1)

    def test_invalid_guess(self):
        self.assertEqual(models.Guess.objects.count(), 0)
        data = {
            'keyword': 'fake_keyword',
            'number': 666,
            'timestamp': datetime.datetime.now(),
        }
        self.assertEqual(tasks.create_guess(data=data), 'KO')

        self.assertEqual(models.Guess.objects.count(), 0)
