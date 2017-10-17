# -*- coding: utf-8 -*-
__author__ = 'buzz'
__date__ = '2017/10/17 下午1:07'

from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish
