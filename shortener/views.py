from django.shortcuts import get_object_or_404, redirect

from .models import URL


def short_redirect(request, slug):
    """Redirect to the permanent URL of a link"""
    url = get_object_or_404(URL, slug=slug)
    url.clicked()

    return redirect(url.full_url)
