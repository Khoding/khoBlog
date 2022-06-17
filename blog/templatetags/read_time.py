import readtime
from django import template

register = template.Library()


def read(html):
    """returns reading time"""
    return readtime.of_html(html)


register.filter("readtime", read)
