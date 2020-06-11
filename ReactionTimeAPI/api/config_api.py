from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND

from ..models import Config
from ..serializers import ConfigSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_all_configurations(request):
    """
    API endpoint for fetching all configurations.

    Returns:
        Configs
    """

    data = {}
    configs = Config.objects.all()
    for config in configs:
        serialized = ConfigSerializer(config).data
        data[config.type] = serialized

    return Response(data, status=HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def save_configuration(request):
    """
    API endpoint for updating configuration.

    Returns:
        Updated configuration
    """

    config_type = request.data.get("type")
    tries = request.data.get("tries")
    min_timeout = request.data.get("minTimeout")
    max_timeout = request.data.get("maxTimeout")

    try:
        config = Config.objects.get(type=config_type)
    except Config.DoesNotExist:
        return Response('Configuration with given type not found', status=HTTP_404_NOT_FOUND)

    try:
        config.tries = tries
        config.minTimeout = min_timeout
        config.maxTimeout = max_timeout
        config.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    serialized = ConfigSerializer(config).data

    return Response(serialized, HTTP_200_OK)