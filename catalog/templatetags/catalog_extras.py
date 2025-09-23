from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


@register.filter(name="usd")
def usd(value):
    """
    Форматирует число как цену в долларах:
    500.00 -> 500$
    500.50 -> 500.5$
    500.10 -> 500.1$
    500.01 -> 500.01$
    """
    try:
        d = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return value
    s = f"{d.normalize():f}".rstrip("0").rstrip(".")
    return f"{s}$"