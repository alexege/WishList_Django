from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),

    url(r'wishes/new$', views.new_wish),
    url(r'create$', views.create_wish),
    url(r'wishes/remove/(?P<wish_id>\d+)$', views.remove_wish),
    url(r'wishes/edit/(?P<wish_id>\d+)$', views.edit_wish),
    url(r'wishes/update$', views.update_wish),
    url(r'wishes/grant/(?P<wish_id>\d+)$', views.grant_wish),
    url(r'wishes/like/(?P<wish_id>\d+)$', views.like_wish),
    url(r'wishes/unlike/(?P<wish_id>\d+)$', views.unlike_wish),

    url(r'wishes/stats/$', views.stats),

    url(r'^logout$', views.logout),
]