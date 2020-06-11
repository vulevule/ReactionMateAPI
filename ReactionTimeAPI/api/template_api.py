from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from ..models import TestsConfigTemplate, RequiredDataTemplate
from ..serializers import TestsConfigTemplateSerializer, RequiredDataTemplateSerializer


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def get_tests_templates(request):
    """
    API endpoint for fetching tests templates.

    Returns:
        Templates
    """

    templates = TestsConfigTemplate.objects.all()
    serialized = TestsConfigTemplateSerializer(templates, many=True).data
    return Response(serialized, status=HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def get_req_data_templates(request):
    """
    API endpoint for fetching required data templates.

    Returns:
        Templates
    """

    templates = RequiredDataTemplate.objects.all()
    serialized = RequiredDataTemplateSerializer(templates, many=True).data
    return Response(serialized, status=HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def save_tests_template(request):
    """
    API endpoint for saving a new tests template.

    Returns:
        Created template
    """

    name = request.data.get("name")
    data = request.data.get("data")

    if data is None or len(data) == 0:
        return Response('At least one configuration must be provided', status=HTTP_400_BAD_REQUEST)

    try:
        template = TestsConfigTemplate(name=name, data=data)
        template.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    serialized = TestsConfigTemplateSerializer(template).data
    return Response(serialized, status=HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated, IsAdminUser,))
def save_req_data_template(request):
    """
    API endpoint for saving a new required data template.

    Returns:
        Created template
    """

    name = request.data.get("name")
    data = request.data.get("data")

    if data is None or len(data) == 0:
        return Response('At least one configuration must be provided', status=HTTP_400_BAD_REQUEST)

    try:
        template = RequiredDataTemplate(name=name, data=data)
        template.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    serialized = RequiredDataTemplateSerializer(template).data
    return Response(serialized, status=HTTP_200_OK)