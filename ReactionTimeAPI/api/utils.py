from ..models import Score
from ..serializers import ScoreSerializer, UserSerializer


def get_full_user(user, include_scores=True):

    data = UserSerializer(user).data

    if include_scores:
        simple = Score.objects.filter(user__username=user.username, type='simple').order_by('-date')
        recognition = Score.objects.filter(user__username=user.username, type='recognition').order_by('-date')
        choice = Score.objects.filter(user__username=user.username, type='choice').order_by('-date')
        discrimination = Score.objects.filter(user__username=user.username, type='discrimination').order_by('-date')

        scores = {
            'simple': ScoreSerializer(simple, many=True).data,
            'recognition': ScoreSerializer(recognition, many=True).data,
            'choice': ScoreSerializer(choice, many=True).data,
            'discrimination': ScoreSerializer(discrimination, many=True).data,
        }

        user_parsed = {
            'username': data['username'],
            'name': data['name'],
            'email': data['email'],
            'created': data['date_joined'],
            'scores': scores
        }

    else:
        user_parsed = {
            'username': data['username'],
            'name': data['name'],
            'email': data['email'],
            'created': data['date_joined']
        }

    return user_parsed
