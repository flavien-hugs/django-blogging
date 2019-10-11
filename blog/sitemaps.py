from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    """docstring for PostSitemap"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def location(self, item):
        return item.get_absolute_url

    def lastmod(self, obj):
        return obj.updated
