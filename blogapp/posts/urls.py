from django.conf.urls import include, url
from django.contrib import admin

from . import views
# from .views import (
#     post_list,
#     post_create,
#     post_detail,
#     post_update,
#     post_delete,
# )


urlpatterns = [
    url(r'^$', views.post_list, name='list'),
    url(r'^create/$', views.post_create),
    url(r'^(?P<id>\d+)/$', views.post_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', views.post_delete),
    #url(r'^posts/$', views.post_home),
]
