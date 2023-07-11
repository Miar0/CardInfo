from django import template
from textwrap import wrap

register = template.Library()


@register.filter
def dividing_numbers(number):
    return ' '.join(wrap(str(number), 4))


@register.filter
def status_color(status):
    if status.lower() == 'active':
        return 'text-success fw-bold'
    elif status.lower() == 'inactive':
        return 'text-info fw-bold'
    elif status.lower() == 'overdue':
        return 'text-danger fw-bold'


@register.filter
def time_conversion(date):
    return date.strftime('%d/%m/%y')


@register.filter
def price_color(price):
    if price > 0:
        return 'text-success'
    elif price < 0:
        return 'text-danger'


@register.filter
def price_plus(price):
    if price > 0:
        return f"+{price}"
    else:
        return price
