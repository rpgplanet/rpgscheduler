# -*- coding: utf-8 -*-

from rpgcommon.settings.base import *

from os.path import dirname, join

import rpgscheduler as project


DEBUG = True
TEMPLATE_DEBUG = DEBUG


ADMINS = (
    ('Almad', 'almad@rpgplanet.cz'),
)
MANAGERS = ADMINS


TIME_ZONE = 'Europe/Prague'

LANGUAGE_CODE = 'cs'

# Site ID
SITE_ID = 4

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

ROOT_URLCONF = 'rpgscheduler.urls'

TEMPLATE_DIRS = (
    join(dirname(project.__file__), 'templates'),
)

#AUTH_PROFILE_MODULE = 'rpgplayer.UserProfile'
#LOGIN_REDIRECT_URL = '/'
SITE_DOMAIN = "akce.rpgplanet.cz"

SESSION_COOKIE_DOMAIN = ".rpgplanet.cz"

VERSION = project.__versionstr__

LOGIN_REDIRECT_URL = '/'

CHERRYPY_TEST_SERVER = True


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "django.middleware.transaction.TransactionMiddleware",

    'rpgcommon.user.middleware.FbAutoLoginMiddleware',
)

