# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 20:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translate_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Project_Assignments',
            new_name='Assignment',
        ),
    ]