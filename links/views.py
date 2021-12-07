from django.shortcuts import get_object_or_404, redirect

from .models import Link


def short_redirect(request, slug):
    url = get_object_or_404(Link, slug=slug)
    return redirect(url.permalink)
