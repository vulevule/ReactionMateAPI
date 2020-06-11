from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE, \
    HTTP_423_LOCKED

from ..models import Experiment, ExperimentResult, Score
from ..serializers import ExperimentSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_experiment(request, pk):
    """
    API endpoint for fetching an experiment with provided ID.

    Returns:
        Experiment
    """

    try:
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        return Response('Experiment with given ID not found', status=HTTP_404_NOT_FOUND)

    if experiment.deleted is True:
        return Response('Experiment with given ID not found', status=HTTP_404_NOT_FOUND)

    if experiment.disabled is True:
        return Response('This experiment is currently unavailable', status=HTTP_423_LOCKED)

    if experiment.expiration < timezone.now():
        return Response('Experiment with given ID already expired', status=HTTP_400_BAD_REQUEST)

    serialized = ExperimentSerializer(experiment).data

    return Response(serialized, status=HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def get_all_experiments(request):
    """
    API endpoint for fetching all experiments.

    Returns:
        Experiments
    """

    experiments = Experiment.objects.filter(deleted=False).order_by('-created')

    serialized = ExperimentSerializer(experiments, many=True).data

    return Response(serialized, status=HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def create_experiment(request):
    """
    API endpoint for creating a new experiment.

    Returns:
        Created experiment
    """

    required_data = request.data.get("requiredData")
    tests_config = request.data.get("testsConfig")
    expiration = request.data.get("expiration")
    allow_multiple_answers = request.data.get("allowMultipleAnswers")
    name = request.data.get("name")

    if tests_config is None or len(tests_config) == 0:
        return Response('At least one test must be provided', status=HTTP_400_BAD_REQUEST)

    if expiration is None:
        return Response('Valid expiration date must be provided', status=HTTP_400_BAD_REQUEST)

    try:
        experiment = Experiment(
            name=name,
            requiredDataConfig=required_data,
            testsConfig=tests_config,
            expiration=expiration,
            allowMultipleAnswers=allow_multiple_answers
        )
        experiment.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    serialized = ExperimentSerializer(experiment).data

    return Response(serialized, HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def update_experiment(request, pk):
    """
    API endpoint for updating an experiment.

    Returns:
        Updated experiment
    """

    required_data = request.data.get("requiredData")
    tests_config = request.data.get("testsConfig")
    expiration = request.data.get("expiration")
    allow_multiple_answers = request.data.get("allowMultipleAnswers")
    disabled = request.data.get("disabled")
    name = request.data.get("name")

    try:
        print('ENTERED')
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        return Response('Experiment with given ID not found', status=HTTP_404_NOT_FOUND)

    if tests_config is None or len(tests_config) == 0:
        return Response('At least one test must be provided', status=HTTP_400_BAD_REQUEST)

    if expiration is None:
        return Response('Valid expiration date must be provided', status=HTTP_400_BAD_REQUEST)

    try:
        experiment.name = name
        experiment.requiredDataConfig = required_data
        experiment.testsConfig = tests_config
        experiment.expiration = expiration
        experiment.allowMultipleAnswers = allow_multiple_answers
        experiment.disabled = disabled
        experiment.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    serialized = ExperimentSerializer(experiment).data

    return Response(serialized, HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def delete_experiment(request, pk):
    """
        API endpoint for logical deleting of an experiment with provided ID.

        Returns:
            HTTP Status
        """

    try:
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        return Response('Experiment with given ID not found', status=HTTP_404_NOT_FOUND)

    if experiment.deleted is True:
        return Response('Experiment with given ID is already deleted', status=HTTP_400_BAD_REQUEST)

    experiment.deleted = True;
    experiment.save()

    return Response(HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def save_experiment_result(request, pk):
    """
    API endpoint for saving a new result for an experiment with provided ID.

    Returns:
        HTTP status
    """

    user_data = request.data.get("requiredData")
    scores = request.data.get("scores")

    first_name = user_data["firstName"]
    last_name = user_data["lastName"]
    email = user_data["email"]

    try:
        experiment = Experiment.objects.get(pk=pk)
    except Experiment.DoesNotExist:
        return Response('Experiment with given ID not found', status=HTTP_404_NOT_FOUND)

    if experiment.expiration < timezone.now():
        return Response('Experiment with given ID already expired', status=HTTP_400_BAD_REQUEST)

    if experiment.allowMultipleAnswers is False:
        try:
            ExperimentResult.objects.get(email=email, experiment=experiment)
            return Response('User with given email already completed this experiment', status=HTTP_406_NOT_ACCEPTABLE)
        except ExperimentResult.DoesNotExist:
            pass

    del user_data["firstName"]
    del user_data["lastName"]
    del user_data["email"]

    try:
        result = ExperimentResult(first_name=first_name, last_name=last_name, email=email, requiredData=user_data, experiment=experiment)
        result.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    try:
        for obj in scores:
            score_type = obj["type"]
            date = obj["date"]
            average = obj["average"]
            best = obj["best"]
            success = obj["success"]

            score = Score(type=score_type, date=date, average=average, best=best, success=success, experimentResult=result)
            score.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    return Response(HTTP_200_OK)
