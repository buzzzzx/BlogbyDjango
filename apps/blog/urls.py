# -*- coding: utf-8 -*-
__author__ = 'buzz'
__date__ = '2017/10/9 下午11:07'

from django.conf.urls import url
from blog.views import post_list, PostDetailView, PostShareView
from .feeds import LastestPostsFeed

urlpatterns = [
    # post views
    # url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^$', post_list, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', post_list, name='post_list_by_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', PostDetailView.as_view(),
        name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', PostShareView.as_view(), name='post_share'),
    url(r'^feed/$', LastestPostsFeed(), name='post_feed')
]