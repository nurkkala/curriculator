from rest_framework import serializers

from .models import *

class KnowledgeAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KnowledgeArea

class KnowledgeUnitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KnowledgeUnit

class LearningOutcomeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LearningOutcome

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course

