import datetime

from rest_framework import response
from rest_framework import status
from rest_framework import views

from guess import serializers
from guess import tasks


class MakeGuessView(views.APIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['timestamp'] = datetime.datetime.now()
        serializer = serializers.GuessSerializer(data=request_data)
        if serializer.is_valid():
            request_status = status.HTTP_202_ACCEPTED
            tasks.create_guess.delay(request_data)
            data = serializer.data
        else:
            request_status = status.HTTP_400_BAD_REQUEST
            data = {'errors': ['Invalid request.']}
        return response.Response(data, status=request_status)
