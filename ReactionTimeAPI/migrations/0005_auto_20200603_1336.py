# Generated by Django 3.0.5 on 2020-06-03 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReactionTimeAPI', '0004_requireddatatemplate_testsconfigtemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='allowMultipleAnswers',
            field=models.BooleanField(default=False),
        ),
    ]