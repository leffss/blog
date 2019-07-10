"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from blog.feeds import AllPostsRssFeed
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

# 网站地图
sitemaps = {
    'post': PostSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'', include('blog.urls', namespace='blog')),
    url(r'', include('blog.urls')),
    url(r'', include('comments.urls')),
    # 记得在顶部引入 AllPostsRssFeed
    url(r'^rss$', AllPostsRssFeed(), name='rss'),
    # url(r'^search/', include('haystack.urls')),
    url(r'^mdeditor/', include('mdeditor.urls')),
    # url(r'mpttcomments', include('django_mptt_comments.urls')),
    # url(r'^captcha/', include('captcha.urls')),

    # 网站地图
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
