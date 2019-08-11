from django.core import validators
from django.db import models


class LuckyCallContest(models.Model):
    keyword = models.CharField(max_length=255)
    result = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def guesses(self):
        return self.guess_set.all()

    @classmethod
    def get_active_contest(cls):
        if not cls.objects.exists():
            return None

        return cls.objects.order_by('created').last()


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
