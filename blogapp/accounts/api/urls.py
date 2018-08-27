from django.conf.urls import include, url
from django.contrib import admin

from . import views
from .views import (
    UserCreateAPIView,
    UserLoginAPIView
)


urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),

    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    # url(r'^create/$', CommentCreateAPIView.as_view(), name='comment_create'),
    #
    # url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='comment_thread'),

    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='comment_delete'),
]
