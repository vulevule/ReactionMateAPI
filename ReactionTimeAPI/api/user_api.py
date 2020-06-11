from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_406_NOT_ACCEPTABLE

from .utils import get_full_user
from ..models import User


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    """
    API endpoint for standard user login.

    Returns:
        Logged user data and a token
    """

    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response('Required data not provided', status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    # Admin can not log in through standard application
    if not user or username is settings.ADMIN_LOGIN:
        return Response('Invalid credentials', status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    user_parsed = get_full_user(user)

    return Response({'token': token.key, 'user': user_parsed}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def admin_login(request):
    """
    API endpoint for admin user login.

    Returns:
        Logged user data and a token
    """

    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response('Required data not provided', status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response('Invalid credentials', status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    user_parsed = get_full_user(user, include_scores=False)

    return Response({'token': token.key, 'user': user_parsed}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    """
    API endpoint for signup.

    Returns:
        Generated token
    """

    username = request.data.get("username")
    password = request.data.get("password")
    name = request.data.get("name")
    email = request.data.get("email")

    if username is None or password is None or name is None or email is None:
        return Response('Required data not provided', status=HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=username)
        return Response('Given username is already taken', status=HTTP_406_NOT_ACCEPTABLE)
    except User.DoesNotExist:
        try:
            user = User.objects.create_user(username=username, password=password, name=name, email=email)
            token, _ = Token.objects.get_or_create(user=user)

            user_parsed = get_full_user(user)

            return Response({'token': token.key, 'user': user_parsed}, status=HTTP_200_OK)
        except Exception as e:
            return Response(str(e), HTTP_400_BAD_REQUEST)
