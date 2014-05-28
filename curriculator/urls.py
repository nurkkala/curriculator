from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'cs2013.views.home', name='all-courses'),
    url(r'^cs2013/', include('cs2013.urls')),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', kwargs={ 'next_page': '/' }, name='logout'),

    url(r'^admin/', include(admin.site.urls))
)
