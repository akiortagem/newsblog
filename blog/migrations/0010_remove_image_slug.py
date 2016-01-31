# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20160116_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='slug',
        ),
    ]
