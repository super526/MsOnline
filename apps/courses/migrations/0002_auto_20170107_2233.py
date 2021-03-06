# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-07 22:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': '\u7ae0\u8282', 'verbose_name_plural': '\u7ae0\u8282'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': '\u89c6\u9891', 'verbose_name_plural': '\u89c6\u9891'},
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='\u8bfe\u7a0b'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='\u8bfe\u7a0b'),
        ),
        migrations.AlterField(
            model_name='video',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson', verbose_name='\u7ae0\u8282'),
        ),
    ]
