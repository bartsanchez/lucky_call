from django.urls import path
from guess import views


urlpatterns = [
    path('', views.MakeGuessView.as_view(), name='make-guess'),
]
