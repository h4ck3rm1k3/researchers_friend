# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0006_auto_20150109_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='typecode',
            field=models.CharField(choices=[('A', 'Administrative Task'), ('S', 'Search')], editable=False, max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='administrativetask',
            name='activity',
            field=models.OneToOneField(parent_link=True, primary_key=True, editable=False, serialize=False, to='researcher.Activity', verbose_name='activity this task inherits from'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='activity',
            field=models.OneToOneField(parent_link=True, primary_key=True, editable=False, serialize=False, to='researcher.Activity', verbose_name='activity this search inherits from'),
            preserve_default=True,
        ),
    ]
