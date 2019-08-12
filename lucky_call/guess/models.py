from django.core import validators
from django.db import models


class LuckyCallContest(models.Model):
    keyword = models.CharField(max_length=255)
    result = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(
        'Guess',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    @property
    def guesses(self):
        return self.guess_set.order_by('timestamp')

    @property
    def unchecked_guesses(self):
        return self.guesses.filter(checked=False)

    @classmethod
    def get_active_contest(cls):
        if not cls.objects.exists():
            return None

        return cls.objects.order_by('created').last()

    def is_winner(self):
        # we could use the divisibility rule for 11 here but it's not
        # so important since we are not adding latency to requests since we
        # are checking the winner in each request (it could lead to
        # performance issues)
        # https://www.mathsisfun.com/divisibility-rules.html
        return self.result % 11 == 0

    def check_winner(self):
        if self.winner:
            return self.winner

        for guess in self.unchecked_guesses:
            if guess.is_correct():
                self.result += guess.number
            guess.checked = True
            guess.save()
            if self.is_winner():
                self.winner = guess
                return guess

            self.save()

        return None


class Guess(models.Model):
    user_email = models.EmailField(unique=True)
    keyword = models.CharField(max_length=255)
    number = models.IntegerField(
        validators=[
            validators.MinValueValidator(100),
            validators.MaxValueValidator(999)
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey(
        LuckyCallContest,
        default=LuckyCallContest.get_active_contest,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    checked = models.BooleanField(default=False)

    def is_correct(self):
        # keyword is considered valid case-insensitive
        return self.keyword.lower() == self.contest.keyword.lower()
