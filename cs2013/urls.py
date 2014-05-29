from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cs2013.views',
    url(r'^course-details/(?P<course_pk>\d+)/$',
        'course_details', name='course-details'),
    url(r'^course-outcomes/(?P<course_pk>\d+)/(?P<page>\d+)/$',
        'course_outcomes', name='course-outcomes'),

    url(r'^know-area/(?P<area_pk>\d+)/$',
        'know_area', name='know-area'),

    url(r'^remove-outcome/(?P<course_pk>\d+)/(?P<outcome_pk>\d+)/$',
        'remove_outcome', name='remove-outcome'),
    url(r'^add-outcome/$', 'add_outcome', name='add-outcome'),
)
