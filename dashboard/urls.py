from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from dashboard.views import dashboard, motions_view
from dashboard.api import StatusDetail, runGroup, runSetter

urlpatterns = [
    url(r'^$', dashboard, name='home'),
    url(r'^motions/(?P<page>[0-9]+)/(?P<untagged>[0-9]+)/(?P<search>[ÖÜØÄÂÁÉÓÚÍÎöüøäâáéóúíîčćšžČĆŠŽa-zA-Z0-9 \-\+!"%\.,]+)/$', motions_view, name='motions_view'),
    url(r'^motions/(?P<page>[0-9]+)/(?P<untagged>[0-9]+)/$', motions_view, name='motions_view'),

    url(r'^api/status/(?P<pk>[0-9]+)/$', StatusDetail.as_view()),

    url(r'^api/runGroup/(?P<pk>[0-9]+)/(?P<group>[\w].+)/$', runSetter, name='runGroup'),
    url(r'^api/runSetter/(?P<pk>[0-9]+)/$', runSetter, name='runSetter'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    ]