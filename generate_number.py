import random
import string
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from core.models import Card


def get_random_card_number():
    number = ''
    for i in range(4):
        number += ''.join(random.sample(string.digits, 4))

    return int(number)


def get_random_card_cvv():
    number = ''.join(random.sample(string.digits, 3))
    return int(number)


def get_random_card_funds():
    number = ''.join(random.sample(string.digits, 6))
    return int(number)


def get_end_date(date, period):
    today = timezone.now()
    end_date = today
    if date == 'Month':
        end_date = today + relativedelta(months=int(period))
    elif date == 'Year':
        end_date = today + relativedelta(years=int(period))
    return end_date


def generate_card(count, series, date, period):
    today = timezone.now()
    for i in range(count):
        Card.objects.create(
            series=series,
            number=get_random_card_number(),
            release_date=today,
            end_date=get_end_date(date, period),
            cvv=get_random_card_cvv(),
            funds=get_random_card_funds(),
            status='Inactive'
        )