from django.contrib import admin

from .models import Config
from .models.experiment import Experiment, ExperimentResult
from .models.score import Score
from .models.templates import RequiredDataTemplate, TestsConfigTemplate
from .models.user import User

admin.site.register(User)
admin.site.register(Score)
admin.site.register(Experiment)
admin.site.register(ExperimentResult)
admin.site.register(RequiredDataTemplate)
admin.site.register(TestsConfigTemplate)
admin.site.register(Config)