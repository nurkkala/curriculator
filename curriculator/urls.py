from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cs2013.views.home', name='home'),

    url(r'^cs2013/', include('cs2013.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
