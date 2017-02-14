# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-09 18:17
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170209_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='images',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=blog.models.generate_upload_path, width_field='width_field'),
        ),
    ]
