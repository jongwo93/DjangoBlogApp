from django.conf.urls import include, url
from django.contrib import admin

from . import views
from .views import (
    CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
)


urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='comment_list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='comment_create'),

    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='comment_thread'),

    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='comment_delete'),
]
