# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'permissions': (('can_view_message', 'Can view message in dashboard'),)},
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(default=b'UR', max_length=2, choices=[(b'UR', b'unread'), (b'R', b'read')]),
        ),
    ]
