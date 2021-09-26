import readtime
from django import template

register = template.Library()


def read(html):
    return readtime.of_html(html)


register.filter("readtime", read)
