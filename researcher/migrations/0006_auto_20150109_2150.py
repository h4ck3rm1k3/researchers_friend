# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0005_auto_20150109_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrativetask',
            name='activity',
            field=models.OneToOneField(serialize=False, primary_key=True, verbose_name='activity this task inherits from', to='researcher.Activity', parent_link=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='search',
            name='activity',
            field=models.OneToOneField(serialize=False, primary_key=True, verbose_name='activity this search inherits from', to='researcher.Activity', parent_link=True),
            preserve_default=True,
        ),
    ]
