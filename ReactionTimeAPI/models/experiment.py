from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from ..utils import one_month_hence


def init_default_name():
    return 'Experiment' + str(len(Experiment.objects.all()))


class Experiment(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    requiredDataConfig = JSONField(default=dict, null=True, blank=True)
    testsConfig = JSONField(default=dict)
    created = models.DateTimeField(default=timezone.now, blank=True)
    expiration = models.DateTimeField(default=one_month_hence, blank=True)
    allowMultipleAnswers = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)

    def clean(self, *args, **kwargs):
        # run the base validation
        super(Experiment, self).clean(*args, **kwargs)

        # Don't allow expiration dates older than now.
        if self.expiration < timezone.now():
            raise ValidationError('Expiration time must be later than now.')


class ExperimentResult(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    requiredData = JSONField(default=dict)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, blank=True)