from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.conf import settings

from .views import view

import base64
import json

analize_basic = settings.PARLALIZE_OAUTH_CLIENT_KEYS[0] + ':' + settings.PARLALIZE_OAUTH_CLIENT_KEYS[1]
data_basic = settings.PARLADATA_OAUTH_CLIENT_KEYS[0] + ':' + settings.PARLADATA_OAUTH_CLIENT_KEYS[1]

login_context = {
    'data_basic': base64.b64encode(data_basic.encode('ascii')),
    'analize_basic': base64.b64encode(analize_basic.encode('ascii')),
    'data_url': settings.PARLADATA_OAUTH_URL,
    'analize_url': settings.PARLALIZE_OAUTH_URL,
}

urlpatterns = [
    url(r'^$', view, name='page-v2'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='page/login.html', extra_context=login_context), name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
