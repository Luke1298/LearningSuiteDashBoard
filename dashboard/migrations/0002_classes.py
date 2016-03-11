# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=10)),
                ('course_grade', models.CharField(max_length=7)),
                ('course_title', models.CharField(max_length=255)),
                ('grade_scale', models.TextField(default='{"A":"93%", "A-":"90%", "B+":"87%", "B":"83%", "B-":"80%", "C+":"77%", "C":"73%", "C-":"70%", "D+":"67%", "D":"63%", "D-":"60%", "E":"0%"}', help_text='Contains a JSON-ified list of grades')),
                ('cid', models.CharField(max_length=255)),
            ],
        ),
    ]