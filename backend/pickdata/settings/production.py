""" production """
import os
from pickdata.settings.common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pickdata_production',
        'USER': 'pickdata',
        'PASSWORD': 'em4s1911',
        'HOST': '211.249.60.9',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    },
    'neo_v1_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'neo_v1',
        'USER': 'neo',
        'PASSWORD': 'em4s1905',
        'HOST': '211.215.18.252',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

STATIC_URL = '/static/'

STATIC_ROOT = ''

STATICFILES_DIRS = (
    os.path.join('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SYSTEM_USER_TOKEN = 'EAAECkTNZAsoEBAHxdA4uyrhozYf1PXwsD8ZBYO32kZBMMIjdWfOP72m2LSFnRVMh96YlFvoV6nTFrJSCCBAmHiu3TNjQVZA6OpDfsiX3T8KLzgCquz3sqFdalnTGJrttTWW2GuHOquxrZBhDPvfO7KRJtQClApbnPHBw1mgYKRwZDZD'

FACEBOOK_APP_ID = 284297631740545
FACEBOOK_APP_SECRET = '5293bf1db679030d5767c855da2accaa'
FACEBOOK_DEFAULT_SCOPE = ['email', 'user_about_me', 'user_birthday', 'user_website']
FACEBOOK_APP_VERSION = 'v2.10'

AD_IMAGE_PATH = os.path.join(PROJECT_DIR, 'static/image/ad/')