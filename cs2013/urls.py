from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cs2013.views',
    url(r'^outcomes/(?P<course_pk>\d+)/(?P<page>\d+)/$', 'outcomes', name='outcomes'),
    url(r'^details/(?P<course_pk>\d+)/$', 'details', name='details'),
    url(r'^remove/(?P<course_pk>\d+)/(?P<outcome_pk>\d+)/$', 'remove_outcome', name='remove')
)
