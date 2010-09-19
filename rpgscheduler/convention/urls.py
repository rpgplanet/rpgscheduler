from django.conf.urls.defaults import *

urlpatterns = patterns('convention.views',
    url(r'^$', 'home'),
)
