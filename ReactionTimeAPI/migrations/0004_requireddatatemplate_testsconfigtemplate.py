# Generated by Django 3.0.5 on 2020-06-03 09:52

import ReactionTimeAPI.models.templates
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReactionTimeAPI', '0003_experiment_allowmultipleanswers'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequiredDataTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=ReactionTimeAPI.models.templates.req_data_default, max_length=50)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='TestsConfigTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=ReactionTimeAPI.models.templates.tests_config_default, max_length=50)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
        ),
    ]