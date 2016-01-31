# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20151218_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=140)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('status', models.CharField(default=b'ur', max_length=2, choices=[(b'UR', b'unread'), (b'R', b'read')])),
            ],
        ),
    ]
