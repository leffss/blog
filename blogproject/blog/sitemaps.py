# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import Post
from django.db.models.aggregates import Count


# 文章聚类
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Post.objects.filter(status='0')

    def lastmod(self, obj):
        return obj.modified_time

