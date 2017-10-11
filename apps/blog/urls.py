# -*- coding: utf-8 -*-
__author__ = 'buzz'
__date__ = '2017/10/9 下午11:07'

from django.conf.urls import url
from blog.views import PostListView, PostDetailView, PostShareView

urlpatterns = [
    # post views
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', PostDetailView.as_view(),
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', PostShareView.as_view(), name='post_share')
]