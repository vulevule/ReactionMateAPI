from django.contrib.postgres.fields import JSONField
from django.db import models


def req_data_default():
    return 'ReqDataTemplate' + str(len(RequiredDataTemplate.objects.all()))


def tests_config_default():
    return 'TestsConfigTemplate' + str(len(TestsConfigTemplate.objects.all()))


class RequiredDataTemplate(models.Model):
    name = models.CharField(max_length=50, default=req_data_default)
    data = JSONField(default=dict)


class TestsConfigTemplate(models.Model):
    name = models.CharField(max_length=50, default=tests_config_default)
    data = JSONField(default=dict)
