from django.db import models


class KnowledgeUnitCoverage(object):
    """Helper class for reporting coverage of knowledge units by courses."""
    def __init__(self, know_unit):
        self.know_unit = know_unit
        self.tier_coverage = [ None,
                               { 'covered': 0, 'total': 0 },
                               { 'covered': 0, 'total': 0 },
                               { 'covered': 0, 'total': 0 } ]
        for outcome in know_unit.learning_outcomes.all():
            self.tier_coverage[outcome.tier]['total'] += 1

    def add_coverage(self, tier):
        self.tier_coverage[tier]['covered'] += 1

    def covered(self, tier):
        return self.tier_coverage[tier]['covered']

    def total(self, tier):
        return self.tier_coverage[tier]['total']


class KnowledgeArea(models.Model):
    abbreviation = models.CharField(max_length=8)
    name = models.CharField(max_length=256)

    class Meta:
        ordering = [ 'abbreviation' ]

    def __unicode__(self):
        return self.name

    def all_outcomes(self):
        return LearningOutcome.objects \
                              .filter(knowledge_unit__knowledge_area=self) \
                              .select_related('knowledge_unit') \
                              .prefetch_related('courses') \
                              .order_by('knowledge_unit', 'seq')

    def tier_n_outcomes(self, n):
        return LearningOutcome.objects \
                              .filter(tier=n, knowledge_unit__knowledge_area=self) \
                              .order_by('knowledge_unit')

    def coverage(self):
        all_coverage = [ ]
        coverage_by_pk = { }

        for know_unit in self.knowledge_units.all():
            coverage = coverage_by_pk[know_unit.pk] = KnowledgeUnitCoverage(know_unit)
            all_coverage.append(coverage)

        for outcome in self.all_outcomes():
            know_unit = outcome.knowledge_unit
            if outcome.courses.count() > 0:
                coverage_by_pk[know_unit.pk].add_coverage(outcome.tier)

        return all_coverage


class KnowledgeUnit(models.Model):
    name = models.CharField(max_length=256)
    tier1_hrs = models.FloatField()
    tier2_hrs = models.FloatField()
    knowledge_area = models.ForeignKey(KnowledgeArea, related_name='knowledge_units')

    def __unicode__(self):
        return self.name


class LearningOutcome(models.Model):
    TIER_CHOICES = (
        (1, 'Tier 1'),
        (2, 'Tier 2'),
        (3, 'Electives') )
    MASTERY_CHOICES = (
        ('F', 'Familiarity'),
        ('U', 'Usage'),
        ('A', 'Assessment') )
    seq = models.IntegerField()
    tier = models.IntegerField(choices=TIER_CHOICES)
    mastery_level = models.CharField(max_length=1, choices=MASTERY_CHOICES)
    description = models.TextField()
    knowledge_unit = models.ForeignKey(KnowledgeUnit, related_name='learning_outcomes')

    class Meta:
        ordering = [ 'seq' ]

    @classmethod
    def tier_display(cls, n):
        """Return the human-readable name for tier n."""
        for pair in cls.TIER_CHOICES:
            if pair[0] == n:
                return pair[1]
        return "UNKNOWN"

    def __unicode__(self):
        return self.description

    def knowledge_area(self):
        return self.knowledge_unit.knowledge_area


class Course(models.Model):
    designation = models.CharField(max_length=256)
    credit_hours = models.IntegerField()
    name = models.CharField(max_length=256)
    learning_outcomes = models.ManyToManyField(LearningOutcome, related_name='courses')
    completed = models.BooleanField()

    class Meta:
        ordering = [ 'designation' ]

    def __unicode__(self):
        return "{} - {}".format(self.designation, self.name)

    def sorted_outcomes(self):
        return self.learning_outcomes.order_by('knowledge_unit',
                                               'knowledge_unit__knowledge_area').all()

    def unbreakable_designation(self):
        return self.designation.replace(' ', '&nbsp;')
