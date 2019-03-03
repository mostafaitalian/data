from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()


@register.filter('abfuscate', is_safe=False)
@stringfilter
def abfuscate_email(value):
    return value.replace('@', ' at ').replace('.', ' dot ')