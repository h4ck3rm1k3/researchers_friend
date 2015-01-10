# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0004_auto_20150109_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assertion',
            old_name='souce',
            new_name='source',
        ),
    ]
