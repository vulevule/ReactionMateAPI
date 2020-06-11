from django.urls import path

from . import api

urlpatterns = [
    path('login', api.login),
    path('adminLogin', api.admin_login),
    path('signup', api.signup),
    path('saveScore', api.save_score),
    path('test/<int:pk>', api.get_experiment),
    path('saveTest/<int:pk>', api.save_experiment_result),
    path('createExperiment', api.create_experiment),
    path('updateExperiment/<int:pk>', api.update_experiment),
    path('deleteExperiment/<int:pk>', api.delete_experiment),
    path('getAllExperiments', api.get_all_experiments),
    path('exportSingle/<int:pk>', api.export_single_experiment_results),
    path('exportMany', api.export_all_results),
    path('getTestsTemplates', api.get_tests_templates),
    path('getReqDataTemplates', api.get_req_data_templates),
    path('saveTestsTemplate', api.save_tests_template),
    path('saveReqDataTemplate', api.save_req_data_template),
    path('getConfigs', api.get_all_configurations),
    path('saveConfig', api.save_configuration),

]