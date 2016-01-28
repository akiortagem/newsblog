# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='publish_on',
            field=models.DateField(default=datetime.datetime(2015, 12, 7, 12, 50, 19, 179790, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(default=b'OK', max_length=2, choices=[(b'DR', b'Draft'), (b'OK', b'Ok to publish')]),
        ),
    ]
