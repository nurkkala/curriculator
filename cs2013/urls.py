from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cs2013.views',
    url(r'^outcomes/(?P<course_pk>\d+)/(?P<page>\d+)/$', 'outcomes', name='outcomes')
)
