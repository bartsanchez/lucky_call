from django.conf import urls

urlpatterns = [
    urls.url(r'', urls.include('guess.urls')),
]
