# -*- coding: utf-8 -*-
from .defaults import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'padskwqjjj32432432409oidsk4fdKPOKrLKDSAeLDmwqd$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEV = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

DATA_URL = 'http://localhost:8000/v1'
ISCI_URL = 'http://localhost:8880'
ANALIZE_URL = 'http://localhost:8080/v1'

GLEJ_URL = 'https://watch.your_parlamter_url.com'
PAGE_URL = 'https://your_parlamter_url.com'

PARLALIZE_API_KEY = "nekijabolteskega"

API_AUTH = ('ivan', 'ivanivan')

SERVER_USER = 'server_name'

SPS_JS = 'https://your_parlamter_url.com/path_to_sps-js.generator'
