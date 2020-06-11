from django.utils import timezone


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


def one_month_hence():
    return timezone.now() + timezone.timedelta(days=30)


def one_year_hence():
    return timezone.now() + timezone.timedelta(days=365)
