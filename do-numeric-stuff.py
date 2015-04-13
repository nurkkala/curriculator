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
course_outcomes = np.zeros((num_outcomes, num_courses), dtype=np.uint16)
print "{} courses, {} outcomes".format(num_courses, num_outcomes)

course_count = outcome_count = 0
for course in Course.objects.all():
    course_count += 1
    for outcome in course.learning_outcomes.all():
        outcome_count += 1
        course_idx = seq_course_map.id_to_idx(course)
        outcome_idx = seq_outcome_map.id_to_idx(outcome)
        course_outcomes[outcome_idx, course_idx] = 1

print "{} courses, {} outcomes".format(course_count, outcome_count)
print "{} courses mapped, {} outcomes mapped".format(seq_course_map.count,
                                                     seq_outcome_map.count)
np.set_printoptions(linewidth=100, edgeitems=12)

print course_outcomes.shape
print course_outcomes

co_outcomes = np.dot(course_outcomes.transpose(), course_outcomes)
print co_outcomes.shape
print co_outcomes

non_empty_courses = seq_course_map.count
non_empty_outcomes = seq_outcome_map.count

for course_idx in range(0, non_empty_courses):
    course = seq_course_map.idx_to_obj(course_idx)
    all_co_courses = [ ]
    for co_course_idx in range(0, non_empty_courses):
        if course_idx == co_course_idx:
            continue            # Skip relationship with self
        weight = co_outcomes[course_idx, co_course_idx]
        if weight > 0:
            all_co_courses.append({ 'weight': weight,
                                    'co_course': seq_course_map.idx_to_obj(co_course_idx) })
    print course
    # nz = np.nonzero(course_outcomes[:, course_idx])[0].tolist()
    # print nz

    # print [ seq_outcome_map.idx_to_obj(x) for x in nz ]

    # print [ seq_outcome_map.idx_to_obj(int(idx))
    #         for idx in np.nditer(np.nonzero(course_outcomes[:, course_idx])) ]


    # for outcome_idx in np.nonzero(course_outcomes[:, course_idx]):
    #     print "    -> {}".format(seq_outcome_map.idx_to_obj(outcome_idx))

    for co_course in sorted(all_co_courses, key=lambda x: x['weight'], reverse=True):
        print "    {:2d} {}".format(co_course['weight'], co_course['co_course'])
