from rest_framework import generics

from guess import models
from guess import serializers


class MakeGuessView(generics.CreateAPIView):
    queryset = models.Guess.objects.all()
    serializer_class = serializers.GuessSerializer
