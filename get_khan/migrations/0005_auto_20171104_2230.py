# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-04 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_khan', '0004_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='big_file',
            field=models.FileField(blank=True, max_length=2048, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='video',
            name='small_file',
            field=models.FileField(blank=True, max_length=2048, null=True, upload_to=''),
        ),
    ]
