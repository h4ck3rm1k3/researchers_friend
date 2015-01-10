# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField(verbose_name='date scheduled')),
                ('completed_date', models.DateField(verbose_name='date completed')),
                ('typecode', models.CharField(choices=[('A', 'Administrative Task'), ('S', 'Search')], max_length=1)),
                ('status', models.CharField(max_length=64, verbose_name='status of activity')),
                ('description', models.TextField(verbose_name='activity description')),
                ('priority', models.PositiveSmallIntegerField(verbose_name='priority of activity')),
                ('comments', models.TextField(blank=True, verbose_name='comments on activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdministrativeTask',
            fields=[
                ('activity', models.OneToOneField(to='researcher.Activity', primary_key=True, verbose_name='activity this task inherits from', serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assertion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('rationale', models.TextField(verbose_name='basis for the assertion')),
                ('disproved', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AssertionAssertion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('sequence_number', models.PositiveSmallIntegerField(default=0, verbose_name='order of low level of assertion')),
                ('assertion_high', models.ForeignKey(to='researcher.Assertion', verbose_name='output assertion', related_name='+')),
                ('assertion_low', models.ForeignKey(to='researcher.Assertion', verbose_name='input assertion', related_name='+')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Characteristic',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(verbose_name='characteristic start date')),
                ('date_end', models.DateField(verbose_name='characteristic end date')),
                ('sort_order', models.CharField(choices=[('A', 'Ascending'), ('D', 'Descending'), ('N', 'None')], max_length=1, verbose_name='how to sort characteristics')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharacteristicPart',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='characteristic part name')),
                ('sequence_number', models.PositiveSmallIntegerField(default=0, verbose_name='order of characteristic part')),
                ('characteristic', models.ForeignKey(to='researcher.Characteristic', verbose_name='characteristic this is a part of')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CharacteristicPartType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name of the type of the characteristic part')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CitationPart',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256, verbose_name='citation part value')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CitationPartType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='citation party name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='event name')),
                ('date_start', models.DateField(verbose_name='event start date')),
                ('date_end', models.DateField(verbose_name='event end date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='event type name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventTypeRole',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='role name')),
                ('event_type', models.ForeignKey(to='researcher.EventType', verbose_name='type of event this role belongs to')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='group name')),
                ('date_start', models.DateField(verbose_name='group start date')),
                ('date_end', models.DateField(verbose_name='group end date')),
                ('criteria', models.TextField(verbose_name='criteria for admission to group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='group type name')),
                ('sort_order', models.CharField(default='A', choices=[('A', 'Ascending'), ('D', 'Descending'), ('N', 'None')], max_length=1, verbose_name='group type sort order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupTypeRole',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='role name')),
                ('sequence_number', models.PositiveSmallIntegerField(default=0, verbose_name='order in which this should appear in list of roles')),
                ('group_type', models.ForeignKey(to='researcher.GroupType', verbose_name='type of group this role pertains to')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='name of the person')),
                ('description_comments', models.TextField(verbose_name='about this person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('existence_date_start', models.DateField(verbose_name='date this place was founded')),
                ('existence_date_end', models.DateField(verbose_name='date this place ceased to be')),
                ('sort_order', models.CharField(default='A', choices=[('A', 'Ascending'), ('D', 'Descending'), ('N', 'None')], max_length=1, verbose_name='order in which to sort place parts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlacePart',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='place part name')),
                ('sequence_number', models.PositiveSmallIntegerField(default=0, verbose_name='order number for this place part type')),
                ('place', models.ForeignKey(to='researcher.Place', verbose_name='place entity this part belongs to')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlacePartType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='place part type name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='project name')),
                ('description', models.TextField(blank=True, verbose_name='project description')),
                ('client_data', models.TextField(blank=True, verbose_name='project client information')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='repository name')),
                ('address', models.TextField(blank=True, verbose_name='repository address')),
                ('phone', models.CharField(blank=True, max_length=64, verbose_name='repository phone number')),
                ('hours', models.TextField(blank=True, verbose_name='repository hours')),
                ('comments', models.TextField(blank=True, verbose_name='comments about the repository')),
                ('place', models.ForeignKey(to='researcher.Place', verbose_name='location of repository')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepositorySource',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('call_number', models.CharField(blank=True, max_length=64, verbose_name='call number for this particular sounce in this repository')),
                ('description', models.TextField(blank=True, verbose_name='notes about this source in this repository')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Representation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('physical_file_code', models.CharField(blank=True, max_length=256, verbose_name='location of the physical representation')),
                ('medium', models.CharField(max_length=64, verbose_name='representation medium')),
                ('comments', models.TextField(blank=True, verbose_name='comments describing the representation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepresentationType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='type of representation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name="researcher's full name")),
                ('comments', models.TextField(blank=True, verbose_name='comments about the researcher')),
                ('address', models.ForeignKey(to='researcher.Place', blank=True, verbose_name="researcher's address place")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResearcherProject',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=64, verbose_name="researcher's role on project")),
                ('project', models.ForeignKey(to='researcher.Project')),
                ('researcher', models.ForeignKey(to='researcher.Researcher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResearchObjective',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='research objective name')),
                ('description', models.TextField(blank=True, verbose_name='research objective descriptin')),
                ('sequence_number', models.PositiveSmallIntegerField(default=0, verbose_name='research objective sequence number')),
                ('priority', models.PositiveSmallIntegerField(verbose_name='research objective priority')),
                ('status', models.CharField(max_length=64, verbose_name='research objective status')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('activity', models.OneToOneField(to='researcher.Activity', primary_key=True, verbose_name='activity this search inherits from', serialize=False)),
                ('searched_for', models.TextField(verbose_name='text searched for')),
                ('repository', models.ForeignKey(to='researcher.RepositorySource', verbose_name='repository searched', related_name='repository_searches')),
                ('source', models.ForeignKey(to='researcher.RepositorySource', verbose_name='source searched', related_name='source_searches')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('subject_date_start', models.DateField(verbose_name='beginning of source date range')),
                ('subject_date_end', models.DateField(verbose_name='ending of source date range')),
                ('comment', models.TextField(blank=True, verbose_name='comments about the source')),
                ('higher_source', models.ForeignKey(to='researcher.Source', blank=True, verbose_name='higher-level source that contains this source')),
                ('jurisdiction_place', models.ForeignKey(to='researcher.Place', verbose_name='place where source was created or stored', related_name='jurisdiction_sources')),
                ('repositories', models.ManyToManyField(to='researcher.Repository', blank=True, through='researcher.RepositorySource', verbose_name='repositories in which this source can be found')),
                ('researcher', models.ForeignKey(to='researcher.Researcher', verbose_name='person who gathered this source record')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='category of sources')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuretyScheme',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='surety scheme name')),
                ('description', models.TextField(blank=True, verbose_name='surety scheme description')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuretySchemePart',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1, verbose_name='surety scheme part name')),
                ('description', models.TextField(blank=True, verbose_name='surety scheme part description')),
                ('sequence_number', models.PositiveSmallIntegerField(default=0, verbose_name='surety part sequence number')),
                ('surety_scheme', models.ForeignKey(to='researcher.SuretyScheme', verbose_name='surety scheme this part belongs to')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='source',
            name='source_group',
            field=models.ManyToManyField(to='researcher.SourceGroup', blank=True, verbose_name='groups or categories this source belongs to'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='subject_place',
            field=models.ForeignKey(to='researcher.Place', verbose_name='place described by the source', related_name='subject_sources'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='researchobjective',
            name='activities',
            field=models.ManyToManyField(to='researcher.Activity', blank=True, verbose_name='activities undertaken to further this objective'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='researchobjective',
            name='project',
            field=models.ForeignKey(to='researcher.Project', verbose_name='project this objective belongs to'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='representation',
            name='representation_type',
            field=models.ForeignKey(to='researcher.RepresentationType', verbose_name='type of document this representation is'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='representation',
            name='source',
            field=models.ForeignKey(to='researcher.Source', verbose_name='source that this represents'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='repositorysource',
            name='activity',
            field=models.ForeignKey(to='researcher.Search', verbose_name='specific search done in this combination'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='repositorysource',
            name='repository',
            field=models.ForeignKey(to='researcher.Repository', blank=True, verbose_name='repository that holds source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='repositorysource',
            name='source',
            field=models.ForeignKey(to='researcher.Source', blank=True, verbose_name='source in repository'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='researchers',
            field=models.ManyToManyField(to='researcher.Researcher', blank=True, through='researcher.ResearcherProject', verbose_name='researchers working on the project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='surety_scheme',
            field=models.ForeignKey(to='researcher.SuretyScheme', blank=True, verbose_name='surety scheme used by the project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='placepart',
            name='place_part_type',
            field=models.ForeignKey(to='researcher.PlacePartType', verbose_name='type of part this is'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='group_type',
            field=models.ForeignKey(to='researcher.GroupType', verbose_name='group type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='place',
            field=models.ForeignKey(to='researcher.Place', blank=True, verbose_name='place associated with this group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(to='researcher.EventType', verbose_name='type of the event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='researcher.Place', verbose_name='where this event took place'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='citationpart',
            name='citation_part_type',
            field=models.ForeignKey(to='researcher.CitationPartType', verbose_name='type that corresponds to this citation part'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='citationpart',
            name='source',
            field=models.ForeignKey(to='researcher.Source', verbose_name='source that this citation part refers to'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='characteristicpart',
            name='characteristic_part_type',
            field=models.ForeignKey(to='researcher.CharacteristicPartType', verbose_name='type of characteristic part'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='characteristic',
            name='place',
            field=models.ForeignKey(to='researcher.Place', verbose_name='place where characteristic was noted'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='researcher',
            field=models.ForeignKey(to='researcher.Researcher', verbose_name='researcher who made assertion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='souce',
            field=models.ForeignKey(to='researcher.Source', verbose_name='source that prompted assertion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assertion',
            name='surety_scheme_part',
            field=models.ForeignKey(to='researcher.SuretySchemePart', blank=True, verbose_name='assertion surety'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='researcher',
            field=models.ForeignKey(to='researcher.Researcher', verbose_name='researcher performing this activity'),
            preserve_default=True,
        ),
    ]
