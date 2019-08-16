import datetime

from factory import django

from guess import models


class LuckyCallContestFactory(django.DjangoModelFactory):
    class Meta:
        model = models.LuckyCallContest
        django_get_or_create = ('keyword',)

    keyword = 'fake_keyword'


class GuessFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Guess
        django_get_or_create = ('user_email',)

    user_email = 'test@example.com'
    keyword = 'fake_keyword'
    number = 666
    timestamp = datetime.datetime.now()
