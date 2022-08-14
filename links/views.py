from django.shortcuts import get_object_or_404, redirect

from .models import Links


def short_redirect(request, slug):
    """Redirect to the permanent URL of a link"""
    url = get_object_or_404(Links, slug=slug)
    return redirect(url.get_absolute_permalink)
