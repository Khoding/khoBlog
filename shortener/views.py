from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test

from .models import URL


@ user_passes_test(lambda u: u.is_superuser)
def root(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    url.clicked()

    return redirect(url.full_url)
