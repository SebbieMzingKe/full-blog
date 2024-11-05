from django.contrib import admin
from django.urls import include,  path
from django.contrib.sitemaps.views import sitemap
from djblog.sitemaps import PostSiteMap, TagSiteMap

sitemaps = {
    'posts': PostSiteMap,
    'tags': TagSiteMap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djblog/', include('djblog.urls', namespace = 'djblog')),
    path(
        'sitemap.xml',
        sitemap,
        {
            'sitemaps': sitemaps
        },
        name = 'django.contrib.sitemaps.views.sitemap'
    ),
]