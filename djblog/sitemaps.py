from django.contrib.sitemaps import Sitemap
from .models import Post
from taggit.models import Tag

class PostSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated

class TagSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Tag.objects.all()  # Return all tags

    def location(self, item):
        return f'/djblog/tags/{item.slug}/' 