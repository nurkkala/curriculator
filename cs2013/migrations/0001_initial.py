# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=256)),
                ('credit_hours', models.IntegerField()),
                ('name', models.CharField(max_length=256)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['designation'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KnowledgeArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['abbreviation'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KnowledgeUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('tier1_hrs', models.FloatField()),
                ('tier2_hrs', models.FloatField()),
                ('knowledge_area', models.ForeignKey(related_name='knowledge_units', to='cs2013.KnowledgeArea')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LearningOutcome',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seq', models.IntegerField()),
                ('tier', models.IntegerField(choices=[(1, b'Tier 1'), (2, b'Tier 2'), (3, b'Electives')])),
                ('mastery_level', models.CharField(max_length=1, choices=[(b'F', b'Familiarity'), (b'U', b'Usage'), (b'A', b'Assessment')])),
                ('description', models.TextField()),
                ('knowledge_unit', models.ForeignKey(related_name='learning_outcomes', to='cs2013.KnowledgeUnit')),
            ],
            options={
                'ordering': ['seq'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='course',
            name='learning_outcomes',
            field=models.ManyToManyField(related_name='courses', to='cs2013.LearningOutcome'),
            preserve_default=True,
        ),
    ]
