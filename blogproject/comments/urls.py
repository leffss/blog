from django.conf.urls import url

from . import views

app_name = 'comments'

urlpatterns = [
    # url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
    url(r'^comment/post/(?P<post_pk>[0-9]+)$', views.post_comment, name='post_comment'),
    url(r'^captcha.png$', views.get_captcha, name="get_captcha"),
    url(r'^captcha-admin.png$', views.get_captcha_admin, name="get_captcha_admin"),
    url(r'^comment/get/(?P<post_pk>[0-9]+)$', views.get_comment, name='get_comment'),
]
