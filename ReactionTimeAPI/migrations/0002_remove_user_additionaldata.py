# Generated by Django 3.0.5 on 2020-05-25 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ReactionTimeAPI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='additionalData',
        ),
    ]
