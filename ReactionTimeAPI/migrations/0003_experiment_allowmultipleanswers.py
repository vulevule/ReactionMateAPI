# Generated by Django 3.0.5 on 2020-05-29 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReactionTimeAPI', '0002_remove_user_additionaldata'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='allowMultipleAnswers',
            field=models.BooleanField(default=True),
        ),
    ]