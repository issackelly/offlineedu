# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-04 17:22
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('get_khan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_modified', models.DateTimeField(auto_now=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('slug', models.CharField(db_index=True, max_length=256)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='get_khan.Topic')),
            ],
        ),
        migrations.RenameField(
            model_name='topictree',
            old_name='modified',
            new_name='local_modified',
        ),
        migrations.AlterField(
            model_name='topictree',
            name='tree',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
