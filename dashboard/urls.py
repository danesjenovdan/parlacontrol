from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from dashboard.views import dashboard
from dashboard.api import StatusDetail, runGroup, runSetter

urlpatterns = [
    url(r'^$', dashboard, name='home'),
    url(r'^api/status/(?P<pk>[0-9]+)/$', StatusDetail.as_view()),

    url(r'^api/runGroup/(?P<pk>[0-9]+)/(?P<group>[\w].+)/$', runSetter, name='runGroup'),
    url(r'^api/runSetter/(?P<pk>[0-9]+)/$', runSetter, name='runSetter'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    ]