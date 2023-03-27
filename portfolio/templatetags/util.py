from django import template

from portfolio.models import Investor

register = template.Library()


@register.filter
def is_investor(value):
    # print(type(value))
    if type(value) != dict:
        value = value.__dict__
    if Investor.objects.filter(individual=value['id']).count():
        return True


@register.filter
def is_founder(value):
    if hasattr(value, 'founder'):
        return True


@register.filter
def is_founder_and_investor(value):
    if is_investor(value) and is_founder(value):
        return True
