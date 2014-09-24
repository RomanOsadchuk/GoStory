from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^', include('general.urls')),
    url(r'^', include('stories.urls')),
    url(r'^auth/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

