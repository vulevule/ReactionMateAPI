# Generated by Django 3.0.5 on 2020-06-08 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReactionTimeAPI', '0008_experimentresult_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
