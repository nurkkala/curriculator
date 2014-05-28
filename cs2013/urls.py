from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cs2013.views',
    url(r'^all-outcomes', 'all_outcomes', name='all-outcomes'),
    url(r'^course-outcomes/(?P<course_pk>\d+)/(?P<page>\d+)/$', 'course_outcomes', name='course-outcomes'),
    url(r'^course-details/(?P<course_pk>\d+)/$', 'course_details', name='course-details'),
    url(r'^remove/(?P<course_pk>\d+)/(?P<outcome_pk>\d+)/$', 'remove_outcome', name='remove-outcome'),
)
