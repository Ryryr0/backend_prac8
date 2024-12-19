from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def get_only_file_name(value):
    return value.split('/')[-1]
