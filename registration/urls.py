from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from .views import RegistrationView, ProfileView


urlpatterns = patterns('',
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', lambda r: logout(r, next_page='/'), name='logout'),
    
    url(r'^profile/(?P<username>[\w-]+)/$', ProfileView.as_view(), name='profile'),
)

