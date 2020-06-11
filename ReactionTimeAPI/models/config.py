from django.core.exceptions import ValidationError
from django.db import models


class Config(models.Model):
    class ConfigTypes(models.TextChoices):
        GENERAL = 'general'
        SIMPLE = 'simple'
        DISCRIMINATION = 'discrimination'
        CHOICE = 'choice'
        RECOGNITION = 'recognition'

    type = models.CharField(choices=ConfigTypes.choices, max_length=20, unique=True)
    minTimeout = models.IntegerField(default=2000)
    maxTimeout = models.IntegerField(default=4000)
    tries = models.IntegerField(default=5)

    def save(self, *args, **kwargs):
        choice = self.type
        if not any(choice in _tuple for _tuple in self.ConfigTypes.choices):
            raise ValidationError('Invalid config type.')
        super(Config, self).save(*args, **kwargs)