from rest_framework import serializers

from guess import models


class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Guess
        fields = '__all__'
