from django.conf.urls.defaults import *

urlpatterns = patterns('convention.views',
    url(r'^$', 'home', name='event-home'),
    url(r'^nova/$', 'new', name='event-new'),
    url(r'^akce/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>.+)/$', 'profile', name='event-profile'),
    url(r'^akce/(?P<event_id>\d+)/program/editace/$', 'agenda_edit', name='agenda-edit'),
)
