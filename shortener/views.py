from django.shortcuts import get_object_or_404, redirect

from .models import URL


def root(request, slug):
    url = get_object_or_404(URL, slug=slug)
    url.clicked()

    return redirect(url.full_url)
