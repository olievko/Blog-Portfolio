from django.contrib.sitemaps import Sitemap
from .models import Post, Project


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Project.published.all()

    def lastmod(self, obj):
        return obj.updated

