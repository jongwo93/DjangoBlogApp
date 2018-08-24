from django.conf.urls import include, url
from django.contrib import admin

from . import views
from .views import (
    comment_thread,
    comment_delete,
)


urlpatterns = [
    # url(r'^$', views.post_list, name='list'),
    # url(r'^create/$', views.post_create),
    url(r'^(?P<id>\d+)/$', comment_thread, name='comment_thread'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='comment_delete'),
    #url(r'^posts/$', views.post_home),
]
