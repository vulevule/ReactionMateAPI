from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from .utils import get_full_user
from ..models import Score


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_score(request):
    """
    API endpoint for saving a new score.

    Returns:
        Logged user data with new score
    """

    user = request.user

    score_type = request.data.get("type")
    date = request.data.get("date")
    average = request.data.get("average")
    best = request.data.get("best")
    success = request.data.get("success")

    if score_type is None or average is None or best is None or success is None:
        return Response('Required data not provided', status=HTTP_400_BAD_REQUEST)

    try:
        score = Score(user=user, type=score_type, date=date, average=average, best=best, success=success)
        score.save()
    except Exception as e:
        return Response(str(e), HTTP_400_BAD_REQUEST)

    return Response(get_full_user(user), HTTP_200_OK)
