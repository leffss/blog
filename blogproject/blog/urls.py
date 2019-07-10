from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'blog'

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    
    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^post/(?P<pk>[0-9]+)$', views.PostDetailView.as_view(), name='detail'),
    url(r'^post/(?P<pk>[0-9]+)$', cache_page(60 * 15)(views.PostDetailView.as_view()), name='detail'),  # 缓存15分钟
    
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    # path('archives/<int:year>/<int:month>/', views.ArchivesView.as_view(), name='archives'),
    re_path(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    # django 2.0 版本后可以使用 re_path, path，以前的 url 就是 re_path
    
    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^category/(?P<pk>[0-9]+)$', views.CategoryView.as_view(), name='category'),
    
    url(r'^tag/(?P<pk>[0-9]+)$', views.TagView.as_view(), name='tag'),
    
    # url(r'^search/$', views.search, name='search'),
    path('search', views.MySearchView.as_view(), name='haystack_search'),

    # url(r'^archives$', views.ArchivesallView.as_view(), name='archives'),
    
    url(r'^about$', views.about, name='about'),
    
    url(r'^series/(?P<pk>[0-9]+)$', views.SeriesView.as_view(), name='series'),

]

