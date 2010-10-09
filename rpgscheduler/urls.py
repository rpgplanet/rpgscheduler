from os.path import dirname, join, normpath

import django
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import ella
from ella import newman

admin.autodiscover()
newman.autodiscover()

#urlpatterns = patterns('',)

ADMIN_ROOTS = (
    normpath(join(dirname(ella.__file__), 'newman', 'media')),
    normpath(join(dirname(django.__file__), 'contrib', 'admin', 'media')),
)

js_info_dict = {
    'packages': ('ella.newman',),
}

from rpgscheduler.convention import urls as conurls
from rpgscheduler.service import urls as serviceurls
from rpgcommon.user import urls as userurls

urlpatterns = patterns('',
    url(r'^uzivatel/', include(userurls, namespace="registration")),
    url(r'^', include(serviceurls, namespace="service")),
    url(r'^', include(conurls, namespace="con")),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # serve newman media static files
        (r'^%s/(?P<path>.*)$' % settings.NEWMAN_MEDIA_PREFIX.strip('/'), 'django.views.static.serve',
            {'document_root': settings.NEWMAN_MEDIA_ROOT, 'show_indexes': True,}),
#        # serve newman static files
        (r'^%s/newman/(?P<path>.*)$' % settings.STATIC_URL.strip('/'), 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True,}),
        # serve static files
        (r'^%s/(?P<path>.*)$' % settings.STATIC_URL.rstrip('/').lstrip('/'), 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        # serve media files
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.rstrip('/').lstrip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

# yes, in tests, models are imported, but not neccessarily when running in production...
# but production must go through http so there so...AAAAAAAARRRRRRRGGGGGHHHHHHHHH!!!!111!
from djangomarkup.register import modify_registered_models
modify_registered_models()
