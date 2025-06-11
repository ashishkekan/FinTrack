from math import isnan

from babel.numbers import format_number
from django import template

register = template.Library()


@register.filter(name="format_big_number")
def format_big_number(number):
    sign = "-" if number < 0 else ""
    number = abs(number)
    if number == 0:
        return "₹0"
    if not number or not str(number).strip():
        return "-"
    elif number < 1_000:
        return f"{sign}₹{number:0.2f}"
    elif number < 1_00_000:
        return f"{sign}₹{number/1_000:0.2f}K"
    elif number < 1_00_00_000:
        return f"{sign}₹{number/1_00_000:0.2f}L"
    elif number < 10_000_00_00_000:
        return f"{sign}₹{number/1_00_00_000:0.2f}Cr"
    number = round(number / 1_00_00_000)
    return f"{sign}₹{number}Cr"


@register.filter(name="format_indian_currency")
def format_indian_currency(number):
    if not number or (isinstance(number, float) and isnan(number)):
        return "₹0"
    try:
        indian_currency_format = format_number(number, locale="en_IN")
    except Exception:
        return "-"
    return "₹" + str(indian_currency_format)
