# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-28 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=28, verbose_name='\u5e74\u9f84'),
        ),
    ]
