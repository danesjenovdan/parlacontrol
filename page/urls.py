from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import view

urlpatterns = [
    url(r'^$', view, name='page-v2'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    ]