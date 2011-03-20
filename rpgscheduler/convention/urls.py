from django.conf.urls.defaults import *

urlpatterns = patterns('convention.views',
    url(r'^$', 'home', name='event-home'),
    url(r'^nova/$', 'new', name='event-new'),
    url(r'^akce/$', 'events_personal', name='events-personal'),
    url(r'^akce/(?P<event_id>\d+)/$', 'profile', name='event-profile'),
    url(r'^akce/(?P<event_id>\d+)/termin/navrhy/$', 'occurrence_proposal', name='event-occurrence-proposal'),
    url(r'^akce/(?P<event_id>\d+)/program/editace/$', 'agenda_edit', name='agenda-edit'),
    url(r'^akce/(?P<event_id>\d+)/program/editace/(?P<agenda_id>\d+)/$', 'agenda_edit', name='agenda-edit'),

    url(r'^akce/(?P<event_id>\d+)/diskuze/nova/$', 'comments_create', name='event-comments-create'),
)
