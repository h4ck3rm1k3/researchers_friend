# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0003_auto_20150109_1452'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'activities'},
        ),
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name_plural': 'repositories'},
        ),
        migrations.AlterModelOptions(
            name='search',
            options={'verbose_name_plural': 'searches'},
        ),
        migrations.AlterField(
            model_name='assertion',
            name='souce',
            field=models.ForeignKey(blank=True, to='researcher.Source', verbose_name='source that prompted assertion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='place',
            name='sort_order',
            field=models.CharField(max_length=1, choices=[('A', 'Ascending'), ('D', 'Descending'), ('N', 'None')], verbose_name='sort direction', default='A'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placepart',
            name='name',
            field=models.CharField(max_length=128, verbose_name='place name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placepart',
            name='place_part_type',
            field=models.ForeignKey(to='researcher.PlacePartType', verbose_name='place type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='placepart',
            name='sequence_number',
            field=models.PositiveSmallIntegerField(verbose_name='sort order', default=0),
            preserve_default=True,
        ),
    ]
