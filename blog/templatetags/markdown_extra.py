from django import template
from django.utils.html import format_html
from markdownx.utils import markdownify

register = template.Library()


@register.filter
def formatted_markdown(text):
    return format_html(markdownify(text))
