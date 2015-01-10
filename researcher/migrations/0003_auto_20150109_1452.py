# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0002_researcher_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='existence_date_end',
            field=models.DateField(verbose_name='date this place ceased to be', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='place',
            name='existence_date_start',
            field=models.DateField(verbose_name='date this place was founded', blank=True),
            preserve_default=True,
        ),
    ]
