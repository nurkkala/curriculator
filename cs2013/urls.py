from django.conf.urls import patterns, url, include

from rest_framework import routers

from cs2013 import views

router = routers.DefaultRouter()
router.register(r'areas', views.KnowledgeAreaViewSet)
router.register(r'units', views.KnowledgeUnitViewSet)
router.register(r'outcomes', views.LearningOutcomeViewSet)
router.register(r'courses', views.CourseViewSet)

urlpatterns = patterns(
    'cs2013.views',

    url(r'^course-details/(?P<course_pk>\d+)/$',
        'course_details', name='course-details'),
    url(r'^course-outcomes/(?P<course_pk>\d+)/(?P<page>\d+)/$',
        'course_outcomes', name='course-outcomes'),

    url(r'^reports/coverage/$',
        'coverage', name='coverage'),

    url(r'^reports/co-outcomes/$',
        'co_outcomes', name='co-outcomes'),

    url(r'^reports/bubbles/$',
        'bubbles', name='bubbles'),

    url(r'^know-area/(?P<area_pk>\d+)/$',
        'know_area', name='know-area'),

    url(r'^remove-outcome/(?P<course_pk>\d+)/(?P<outcome_pk>\d+)/$',
        'remove_outcome', name='remove-outcome'),
    url(r'^add-outcome/$', 'add_outcome', name='add-outcome'),

    url(r'^api/coverage/(?P<tier>[123])/$', views.ListCoverage.as_view(), name='list-coverage'),
    url(r'^api/', include(router.urls)),
    url(r'^swag/', include('rest_framework_swagger.urls')),
)
