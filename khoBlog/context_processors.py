from django.conf import settings


def context(request):
    debug_flag = settings.DEBUG
    context = {
        'CANONICAL_PATH': request.build_absolute_uri(request.path),
        'debug_flag': debug_flag
    }

    return context
