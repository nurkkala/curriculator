#!/usr/bin/env python

import csv

from django.utils.encoding import smart_text

from cs2013.models import *

def import_knowledge_areas():
    with open('resources/knowledge-areas.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            KnowledgeArea.objects.create(abbreviation=row[0], name=row[1])

def import_courses():
    with open('resources/courses.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            Course.objects.create(designation=row[0],
                                  credit_hours=int(row[1]),
                                  name=row[2])
            print "Imported", row[2]

def import_learning_outcomes():
    with open('resources/learning-outcomes.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == '':
                continue        # No data
            if row[0] == 'KA' and row[1] == 'KU':
                continue        # Header

            row = [ smart_text(s.strip(), encoding="ISO-8859-1") for s in row ]

            try:
                ka = KnowledgeArea.objects.get(abbreviation=row[0])
            except KnowledgeArea.DoesNotExist:
                print "No KA with abbreviation '{}'".format(row[0])
                exit(1)

            if row[4] == '' and row[5] == '':
                # New Knowledge Unit
                tier1_hrs = float(row[2])
                tier2_hrs = float(row[3])
                ku, created = KnowledgeUnit.objects.get_or_create(name=row[1],
                                                                  tier1_hrs=tier1_hrs,
                                                                  tier2_hrs=tier2_hrs,
                                                                  knowledge_area=ka)
                print "{} KU".format("Created" if created else "Found"), row[1]
                continue

            # Learning outcome
            try:
                ku = KnowledgeUnit.objects.get(name=row[1], knowledge_area=ka)
            except KnowledgeUnit.DoesNotExist:
                print "No KU with name '{}'".format(row[1])
                exit(1)

            LearningOutcome.objects.create(seq=int(row[4]),
                                           tier=int(row[2]),
                                           mastery_level=row[3][0],
                                           description=row[5],
                                           knowledge_unit=ku)
            print "\tOutcome", row[5]


import_courses()
import_knowledge_areas()
import_learning_outcomes()
