from django.db import models


class KnowledgeArea(models.Model):
    abbreviation = models.CharField(max_length=8)
    name = models.CharField(max_length=256)

    class Meta:
        ordering = [ 'abbreviation' ]

    def __unicode__(self):
        return self.name

    def tier_n_outcomes(self, n):
        return LearningOutcome.objects \
                              .filter(tier=n, knowledge_unit__knowledge_area=self) \
                              .order_by('knowledge_unit')


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
        (3, 'Elective') )
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

    def __unicode__(self):
        return self.description


class Course(models.Model):
    designation = models.CharField(max_length=256)
    credit_hours = models.IntegerField()
    name = models.CharField(max_length=256)
    learning_outcomes = models.ManyToManyField(LearningOutcome, related_name='courses')

    class Meta:
        ordering = [ 'designation' ]

    def __unicode__(self):
        return "{} - {}".format(self.designation, self.name)


