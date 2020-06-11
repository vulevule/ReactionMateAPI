from rest_framework import serializers

from .models import Experiment, User, Score, ExperimentResult, RequiredDataTemplate, TestsConfigTemplate, Config


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        # fields = '__all__'
        exclude = ['user']


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'


class ExperimentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentResult
        fields = '__all__'


class RequiredDataTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDataTemplate
        fields = '__all__'


class TestsConfigTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestsConfigTemplate
        fields = '__all__'


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'