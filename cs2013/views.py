from __future__ import division

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rest_framework import viewsets

from .models import *
from .serializers import *

@login_required
def home(request):
    return render(request, 'cs2013/home.html',
                  { 'courses': Course.objects.all() })

@login_required
def know_area(request, area_pk):
    return render(request, 'cs2013/know_areas.html',
                  { 'all_areas': KnowledgeArea.objects.all(),
                    'selected_area': KnowledgeArea.objects.get(pk=area_pk),
                    'all_courses': Course.objects.all() })

@login_required
def course_outcomes(request, course_pk, page):
    course = Course.objects.get(pk=course_pk)
    know_areas = KnowledgeArea.objects.all()
    outcome_selectors = [ { 'area': area, 'tier': t } for t in [ 1, 2, 3 ] for area in know_areas ]
    page_count = len(outcome_selectors)
    page = max(1, min(int(page), page_count))

    if request.method == 'POST':
        # Update to database
        for outcome_pk in request.POST.getlist('outcome-pk'):
            outcome = LearningOutcome.objects.get(pk=outcome_pk)
            course.learning_outcomes.add(outcome)

        if page == page_count:
            course.completed = True
            course.save()
            return redirect('all-courses')
        else:
            page += 1

    outcome_selector = outcome_selectors[page - 1]
    know_area = outcome_selector['area']
    tier = outcome_selector['tier']
    outcomes = know_area.tier_n_outcomes(tier)

    return render(request, 'cs2013/outcomes.html',
                  { 'course': course,
                    'know_area': know_area,
                    'tier_display': LearningOutcome.tier_display(tier),
                    'outcomes': outcomes,
                    'page': page,
                    'page_count': page_count,
                    'percent': "{:.0f}%".format(page / page_count * 100)
                })

@login_required
def course_details(request, course_pk):
    return render(request, 'cs2013/details.html',
                  { 'course': Course.objects.get(pk=course_pk) })

@login_required
def remove_outcome(request, course_pk, outcome_pk):
    course = Course.objects.get(pk=course_pk)
    outcome = LearningOutcome.objects.get(pk=outcome_pk)
    course.learning_outcomes.remove(outcome)
    return redirect('course-details', course_pk)

@login_required
def add_outcome(request):
    course_pk = request.POST['course_pk']
    outcome_pk = request.POST['outcome_pk']

    course = Course.objects.get(pk=course_pk)
    outcome = LearningOutcome.objects.get(pk=outcome_pk)

    course.learning_outcomes.add(outcome)
    return HttpResponse("Added outcome {} to course {}".format(outcome_pk, course_pk))


def coverage_by_tier():
    """TODO: Should refactor outcome stuff from models file."""
    tier_coverage = [ { 'covered': 0, 'total': 0 }, # All tiers
                      { 'covered': 0, 'total': 0 },
                      { 'covered': 0, 'total': 0 },
                      { 'covered': 0, 'total': 0 } ]

    for outcome in LearningOutcome.objects.all():
        tier_coverage[outcome.tier]['total'] += 1
        tier_coverage[0]['total'] += 1
        if outcome.courses.count() > 0:
            tier_coverage[outcome.tier]['covered'] += 1
            tier_coverage[0]['covered'] += 1

    return tier_coverage

@login_required
def coverage(request):
    knowledge_areas = KnowledgeArea.objects.prefetch_related('knowledge_units').all()
    return render(request, 'cs2013/coverage.html',
                  { 'knowledge_areas': knowledge_areas })

#### API ################################################################

class KnowledgeAreaViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeArea.objects.all()
    serializer_class = KnowledgeAreaSerializer

class KnowledgeUnitViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeUnit.objects.all()
    serializer_class = KnowledgeUnitSerializer

class LearningOutcomeViewSet(viewsets.ModelViewSet):
    queryset = LearningOutcome.objects.all()
    serializer_class = LearningOutcomeSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
