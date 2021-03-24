from django.conf import settings
from django.urls.base import reverse_lazy


def context(request):
    debug_flag = settings.DEBUG
    context = {
        'CANONICAL_PATH': request.build_absolute_uri(request.path),
        'debug_flag': debug_flag,
        'search_url': reverse_lazy('blog:search_results')
    }

    return context
