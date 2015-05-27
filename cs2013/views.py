from __future__ import division
import textwrap

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

import numpy as np
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.views import Response

from .models import *
from .serializers import *
from .forms import *

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

class SequentialMap(object):
    def __init__(self):
        self.next_idx = 0
        self.id_to_idx_map = { }
        self.idx_to_obj_map = { }

    def id_to_idx(self, obj):
        idx = None
        if obj.id in self.id_to_idx_map:
            idx = self.id_to_idx_map[obj.id]
        else:
            idx = self.id_to_idx_map[obj.id] = self.next_idx
            self.next_idx += 1
            self.idx_to_obj_map[idx] = obj
        return idx

    def idx_to_obj(self, idx):
        return self.idx_to_obj_map[idx]

    @property
    def count(self):
        return self.next_idx

@login_required
def co_outcomes(request):
    seq_course_map = SequentialMap()
    seq_outcome_map = SequentialMap()

    num_courses = Course.objects.count()
    num_outcomes = LearningOutcome.objects.count()
    outcome_matrix = np.zeros((num_outcomes, num_courses), dtype=np.uint16)

    course_count = outcome_count = 0
    for course in Course.objects.all():
        course_count += 1
        for outcome in course.learning_outcomes.all():
            outcome_count += 1
            course_idx = seq_course_map.id_to_idx(course)
            outcome_idx = seq_outcome_map.id_to_idx(outcome)
            outcome_matrix[outcome_idx, course_idx] = 1

    # Do the "RTR" calculation
    co_outcomes = np.dot(outcome_matrix.transpose(), outcome_matrix)

    non_empty_courses = seq_course_map.count
    non_empty_outcomes = seq_outcome_map.count

    course_id = 0
    co_course_id = 0
    context = { 'courses': [ ] }

    for course_idx in range(0, non_empty_courses):
        course = seq_course_map.idx_to_obj(course_idx)
        outcome_row = outcome_matrix[:, course_idx]
        outcome_indexes = np.nonzero(outcome_row)[0]

        co_course_data = [ ]
        for co_course_idx in range(0, non_empty_courses):
            if course_idx == co_course_idx:
                continue            # Skip relationship with self
            weight = co_outcomes[course_idx, co_course_idx]
            if weight > 0:
                co_course_data.append({ 'weight': weight,
                                        'co_course_idx': co_course_idx })

        context_co_course_data = [ ]
        for co_course_datum in sorted(co_course_data, key=lambda x: x['weight'], reverse=True):
            weight = co_course_datum['weight']
            co_course_idx = co_course_datum['co_course_idx']

            co_outcome_row = outcome_matrix[:, co_course_idx]
            co_outcome_indexes = np.nonzero(co_outcome_row)[0]
            common_outcome_indexes = np.intersect1d(outcome_indexes, co_outcome_indexes)

            outcomes = [ seq_outcome_map.idx_to_obj(idx) for idx in common_outcome_indexes ]

            context_co_course_data.append({ 'course': seq_course_map.idx_to_obj(co_course_idx),
                                            'weight': weight,
                                            'outcomes': outcomes,
                                            'unique_id': co_course_id })
            co_course_id += 1

        context['courses'].append({ 'course': course,
                                    'co_courses': context_co_course_data,
                                    'unique_id': course_id })
        course_id += 1

    return render(request, 'cs2013/co_outcomes.html', context)

@login_required
def bubbles(request):
    return render(request, 'cs2013/bubbles.html', { })

def coverage_for_selected_courses(query_dict):
    all_outcomes = { }
    for outcome in LearningOutcome.objects \
                                  .all() \
                                  .select_related('knowledge_unit__knowledge_area'):
        all_outcomes[outcome.id] = outcome

    outcome_id_covered = { }
    courses_selected = 0
    for course in Course.objects.all():
        if course.designation in query_dict:
            courses_selected += 1
            for outcome in course.learning_outcomes.all():
                outcome_id_covered[outcome.id] = 1

    coverage = { }
    for tier in (1, 2, 3):
        coverage[tier] = { 'name': LearningOutcome.tier_display(tier),
                           'outcomes_covered': [ ],
                           'outcomes_not_covered': [ ] }

    for outcome in all_outcomes.itervalues():
        if outcome.id in outcome_id_covered:
            coverage[outcome.tier]['outcomes_covered'].append(outcome)
        else:
            coverage[outcome.tier]['outcomes_not_covered'].append(outcome)

    def percent_covered(count_covered, count_not_covered):
        total = count_covered + count_not_covered
        if total == 0:
            percent = 0
        else:
            percent = count_covered / total * 100.0
        return '{:.2f}%'.format(percent)

    for tier in coverage.itervalues():
        tier['count_covered'] = len(tier['outcomes_covered'])
        tier['count_not_covered'] = len(tier['outcomes_not_covered'])
        tier['percent_coverage'] = percent_covered(tier['count_covered'],
                                                   tier['count_not_covered'])
    return courses_selected, [ coverage[i] for i in (1, 2, 3) ]

@login_required
def what_if(request):

    def split_into_sublists(arr, n):
        "Split 'arr' into sublists each containing 'n' elements."
        return [arr[i : i + n] for i in range(0, len(arr), n)]

    coverage = [ ]
    courses_selected = None

    if request.method == 'POST':
        form = CourseCheckForm(request.POST)
        courses_selected, coverage = coverage_for_selected_courses(request.POST)
    else:
        form = CourseCheckForm()

    all_fields = [ field for field in form ]
    form_field_groups = split_into_sublists(all_fields, 9)

    return render(request, 'cs2013/what_if.html',
                  { 'form_field_groups' : form_field_groups,
                    'courses_selected' : courses_selected,
                    'coverage': coverage })

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

class ListCoverage(APIView):
    def get(self, request, tier, format=None):
        areas = { }
        for area in KnowledgeArea.objects.all():
            areas[area.id] = { 'id': area.id,
                               'name': area.name,
                               'abbreviation': area.abbreviation,
                               'outcomes': [ ],
                               'courses': { } }

        for outcome in LearningOutcome.objects \
                                      .filter(tier=tier) \
                                      .select_related('knowledge_unit__knowledge_area') \
                                      .prefetch_related('courses'):
            area_id = outcome.knowledge_unit.knowledge_area.id
            areas[area_id]['outcomes'].append(outcome.id)

            for course in outcome.courses.all():
                if course.id not in areas[area_id]['courses']:
                    areas[area_id]['courses'][course.id] = {
                        'id': course.id,
                        'designation': course.designation,
                        'outcomes': [ ] }
                areas[area_id]['courses'][course.id]['outcomes'].append(outcome.id)

        # Flatten dictionaries into lists.
        for area in areas.itervalues():
            area['courses'] = area['courses'].values()

        return Response(areas.itervalues())
