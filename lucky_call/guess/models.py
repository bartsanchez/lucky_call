from django.core import validators
from django.db import models


class Guess(models.Model):
    user_id = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    number = models.IntegerField(
        validators=[
            validators.MinValueValidator(100),
            validators.MaxValueValidator(999)
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
