from django.conf.urls.defaults import *

urlpatterns = patterns('convention.views',
    url(r'^$', 'home', name='event-home'),
    url(r'^nova/$', 'new', name='event-new'),
)
