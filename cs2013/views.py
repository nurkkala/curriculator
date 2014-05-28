from __future__ import division

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import *

@login_required
def home(request):
    return render(request, 'cs2013/home.html',
                  { 'courses': Course.objects.all() })

@login_required
def all_outcomes(request):
    return render(request, 'cs2013/all_outcomes.html')

@login_required
def course_outcomes(request, course_pk, page):
    course = Course.objects.get(pk=course_pk)
    know_areas = KnowledgeArea.objects.all()
    outcome_selectors = [ { 'area': area, 'tier': t } for t in [ 1, 2 ] for area in know_areas ]
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
            return redirect('home')
        else:
            page += 1

    outcome_selector = outcome_selectors[page - 1]
    know_area = outcome_selector['area']
    tier = outcome_selector['tier']
    outcomes = know_area.tier_n_outcomes(tier)

    return render(request, 'cs2013/outcomes.html',
                  { 'course': course,
                    'know_area': know_area,
                    'tier': tier,
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
    return redirect('details', course_pk)
