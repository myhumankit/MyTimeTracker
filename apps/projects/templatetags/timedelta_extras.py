from datetime import timedelta
from django import template

register = template.Library()


@register.filter
def date_format(value):
    zero = timedelta()
    if value == zero:
        return ""

    days = value.days
    seconds = value.seconds

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    h += days * 24

    texte = f"{h:d}h{m:02d}"

    if value < zero:
        return '<span class="text-danger">{}</span>'.format(texte)
    else:
        return texte
