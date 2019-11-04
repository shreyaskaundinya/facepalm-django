from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter(name="from_index")
@stringfilter
def from_index(string, number):
    return string[number:]
