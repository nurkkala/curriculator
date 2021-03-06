import textwrap

import django
django.setup()

import numpy as np

from cs2013.models import Course, LearningOutcome

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


seq_course_map = SequentialMap()
seq_outcome_map = SequentialMap()

num_courses = Course.objects.count()
num_outcomes = LearningOutcome.objects.count()
outcome_matrix = np.zeros((num_outcomes, num_courses), dtype=np.uint16)
print "{} courses, {} outcomes".format(num_courses, num_outcomes)

course_count = outcome_count = 0
for course in Course.objects.all():
    course_count += 1
    for outcome in course.learning_outcomes.all():
        outcome_count += 1
        course_idx = seq_course_map.id_to_idx(course)
        outcome_idx = seq_outcome_map.id_to_idx(outcome)
        outcome_matrix[outcome_idx, course_idx] = 1

print "{} courses, {} outcomes".format(course_count, outcome_count)
print "{} courses mapped, {} outcomes mapped".format(seq_course_map.count,
                                                     seq_outcome_map.count)
np.set_printoptions(linewidth=100, edgeitems=12)

print outcome_matrix.shape
print outcome_matrix

co_outcomes = np.dot(outcome_matrix.transpose(), outcome_matrix)
print co_outcomes.shape
print co_outcomes

non_empty_courses = seq_course_map.count
non_empty_outcomes = seq_outcome_map.count

wrapper = textwrap.TextWrapper(width=90,
                               initial_indent="      * ",
                               subsequent_indent=" "*8)

for course_idx in range(0, non_empty_courses):
    course = seq_course_map.idx_to_obj(course_idx)
    outcome_row = outcome_matrix[:, course_idx]
    outcome_indexes = np.nonzero(outcome_row)[0]

    print course

    co_course_data = [ ]
    for co_course_idx in range(0, non_empty_courses):
        if course_idx == co_course_idx:
            continue            # Skip relationship with self
        weight = co_outcomes[course_idx, co_course_idx]
        if weight > 0:
            co_course_data.append({ 'weight': weight,
                                    'co_course_idx': co_course_idx })

    for co_course_datum in sorted(co_course_data, key=lambda x: x['weight'], reverse=True):
        weight = co_course_datum['weight']
        co_course_idx = co_course_datum['co_course_idx']

        co_outcome_row = outcome_matrix[:, co_course_idx]
        co_outcome_indexes = np.nonzero(co_outcome_row)[0]
        common_outcome_indexes = np.intersect1d(outcome_indexes, co_outcome_indexes)

        print "   {:2d} {}".format(weight, seq_course_map.idx_to_obj(co_course_idx))
        for common_outcome_index in common_outcome_indexes:
            outcome = seq_outcome_map.idx_to_obj(common_outcome_index)
            print wrapper.fill("{} {} ({}): {}".format(
                outcome.knowledge_unit.knowledge_area.abbreviation,
                outcome.get_tier_display(),
                outcome.get_mastery_level_display(),
                outcome.description))

    print
