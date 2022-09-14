from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect

from .models import URL


def short_redirect(request, slug):
    """Redirect to the permanent URL of a link"""
    current_site = get_current_site(request)
    url = get_object_or_404(URL, slug=slug)
    url.clicked()
    redirect_url = f"{request.scheme}://{current_site.domain}{url.full_url}"
    return redirect(redirect_url)
