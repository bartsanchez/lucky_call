from lucky_call.celery import app

from guess import serializers


@app.task()
def create_guess(data):
    serializer = serializers.GuessSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return 'OK'
    return 'KO'
