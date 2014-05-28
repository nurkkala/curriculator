from __future__ import division

from django.shortcuts import render, redirect

from .models import *

def home(request):
    return render(request, 'cs2013/home.html',
                  { 'courses': Course.objects.all() })

def outcomes(request, course_pk, page):
    course = Course.objects.get(pk=course_pk)
    know_areas = KnowledgeArea.objects.all()
    outcome_selectors = [ { 'area': area, 'tier': t } for t in [ 1, 2 ] for area in know_areas ]
    page_count = len(outcome_selectors)
    page = max(1, min(int(page), page_count))

    if request.method == 'POST':
        # Update to database
        for outcome_pk in request.POST.getlist('outcome-pk'):
            print outcome_pk
            outcome = LearningOutcome.objects.get(pk=outcome_pk)
            course.learning_outcomes.add(outcome)

        if page == page_count:
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
