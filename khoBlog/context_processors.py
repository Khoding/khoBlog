from django.conf import settings
from django.urls.base import reverse
from django.utils import timezone


def context(request):
    debug_flag = settings.DEBUG
    context = {
        'CANONICAL_PATH': request.build_absolute_uri(request.path),
        'debug_flag': debug_flag,
        'search_url': reverse('blog:search_results'),
        'now': timezone.now()
    }

    return context
