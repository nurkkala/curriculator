from django.contrib import admin

from .models import *


class LearningOutcomeInline(admin.TabularInline):
    model = LearningOutcome

class KnowledgeUnitInline(admin.TabularInline):
    model = KnowledgeUnit

class KnowledgeAreaAdmin(admin.ModelAdmin):
    inlines = [ KnowledgeUnitInline ]

class KnowledgeUnitAdmin(admin.ModelAdmin):
    list_filter = [ 'knowledge_area' ]
    inlines = [ LearningOutcomeInline ]


admin.site.register(KnowledgeArea, KnowledgeAreaAdmin)
admin.site.register(KnowledgeUnit, KnowledgeUnitAdmin)
admin.site.register(LearningOutcome)
admin.site.register(Course)
