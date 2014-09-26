# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='added_at',
            field=models.DateTimeField(default=datetime.date(2014, 9, 25), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chapter',
            name='bookmarkers',
            field=models.ManyToManyField(related_name=b'bookmarks', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='dislikers',
            field=models.ManyToManyField(related_name=b'disliked_chapters', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='likers',
            field=models.ManyToManyField(related_name=b'liked_chapters', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chapter',
            name='readers',
            field=models.ManyToManyField(related_name=b'read_chapters', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
    ]
