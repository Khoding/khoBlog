from django.conf import settings
from django.urls.base import reverse
from django.utils import timezone


def context(request):
    debug_flag = settings.DEBUG
    context = {
        'CANONICAL_PATH': request.build_absolute_uri(request.path),
        'debug_flag': debug_flag,
        'search_url': reverse('blog:search_results'),
        'now': timezone.now(),
        'description': "Khodok's Blog was a simple test for Django for school at first before Khodok (the dev of this stupid website) started to like it and continued it as a personal project",
    }

    return context
