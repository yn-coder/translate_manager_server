# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 22:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('readed_at', models.DateTimeField(blank=True, null=True)),
                ('msg_txt', models.CharField(max_length=255)),
                ('msg_url', models.URLField(blank=True, max_length=75, null=True)),
                ('reciever_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciever_user', to=settings.AUTH_USER_MODEL)),
                ('sender_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('state', models.PositiveSmallIntegerField(choices=[(0, 'DRAFT'), (1, 'PUBLISHED'), (2, 'IN PROCESS'), (3, 'DONE'), (4, 'ARCHIVE'), (5, 'CANCEL')], default=0)),
                ('language_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='language_from', to='translate_manager.Language')),
                ('language_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='language_to', to='translate_manager.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Project_Assignments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invited_at', models.DateTimeField(blank=True, null=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('dismissed_at', models.DateTimeField(blank=True, null=True)),
                ('assigned_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translate_manager.Project')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='project_assignments',
            unique_together=set([('project', 'assigned_user')]),
        ),
    ]
