from os.path import dirname, join, abspath

import rpgscheduler as project
import ella

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ENABLE_DEBUG_URLS = DEBUG

SECRET_KEY = 'tlucebubenicektlucenabuben$$$'

FACEBOOK_APPLICATION_ID = '147869781892995'
GOOGLE_ANALYTICS_CODE = 'UA-18615782-1'

STATIC_ROOT = join(dirname(project.__file__), 'static')

ADMIN_MEDIA_PREFIX = '/static/admin_media/'
NEWMAN_MEDIA_PREFIX = '/static/newman_media/'

NEWMAN_MEDIA_ROOT = abspath(join(dirname(ella.__file__), 'newman', 'media'))

CACHE_BACKEND = 'dummy://'
CACHE_TIMEOUT = 10*60
CACHE_SHORT_TIMEOUT = 1*60
CACHE_LONG_TIMEOUT = 60*60

#SESSION_COOKIE_DOMAIN = '.rpgplanet.cz'

