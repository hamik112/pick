""" development """
import os
from a3tio_ad_fb_pickdata.settings.common import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pickdata_v2_development',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
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

SYSTEM_USER_TOKEN = 'EAAUsxsN1snQBAHss8zEYNWpegIrZCLiOzZASUoAAyR177teuCatcjFdTRHSZBKrsRz06tAGVDpmra3UEwjaRwxxg0QCJ7qDyOpGzt5G4z7wTnDDctQZCFSlNcLf5222gRJsKkEscRgv6tkIggAiV8zY9jmhQSpAWYkMWmEqSUwZDZD'

FACEBOOK_APP_ID = 1456607077970548
FACEBOOK_APP_SECRET = 'e74075b09b2854a21a32c79cdad67c60'
FACEBOOK_DEFAULT_SCOPE = ['email', 'user_about_me', 'user_birthday', 'user_website']
FACEBOOK_APP_VERSION = 'v2.10'

AD_IMAGE_PATH = 'static/image/ad/'