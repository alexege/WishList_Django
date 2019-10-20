from django.conf.urls import url, include
urlpatterns = [
    url(r'^', include('apps.wish_app.urls')),
]
