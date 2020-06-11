from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .experiment import ExperimentResult


class Score(models.Model):
    class ScoreTypes(models.TextChoices):
        SIMPLE = 'simple'
        DISCRIMINATION = 'discrimination'
        CHOICE = 'choice'
        RECOGNITION = 'recognition'

    type = models.CharField(choices=ScoreTypes.choices, max_length=20)
    average = models.FloatField()
    best = models.FloatField()
    success = models.FloatField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    experimentResult = models.ForeignKey(ExperimentResult, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        choice = self.type
        if not any(choice in _tuple for _tuple in self.ScoreTypes.choices):
            raise ValidationError('Invalid score type.')
        super(Score, self).save(*args, **kwargs)