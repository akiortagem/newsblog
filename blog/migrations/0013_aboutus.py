# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-21 12:00
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_imagegallery_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', tinymce.models.HTMLField()),
                ('image', models.ImageField(default=b'media/no-img.jpg', upload_to=b'media/')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'Image Gallery',
            },
        ),
    ]