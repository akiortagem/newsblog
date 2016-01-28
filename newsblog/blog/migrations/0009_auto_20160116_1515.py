# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_auto_20160103_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('image', models.ImageField(default=b'media/no-img.jpg', upload_to=b'media/')),
                ('caption', models.CharField(unique=True, max_length=140)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'Image',
            },
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(to='blog.Image')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'Image Gallery',
            },
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-id'], 'permissions': (('can_view_message', 'Can view message in dashboard'),)},
        ),
    ]
