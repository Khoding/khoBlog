from django.conf import settings
from django.utils import timezone


def context(request):
    debug_flag = settings.DEBUG
    comments_disabled_globally_flag = settings.COMMENTS_DISABLED_GLOBALLY
    context = {
        "CANONICAL_PATH": request.build_absolute_uri(request.path_info),
        "debug_flag": debug_flag,
        "now": timezone.now(),
        "description": "Welcome to my website, it's a blog, a portfolio, a personal playground, and too much time is dedicated to it.",
        "comments_disabled_globally_flag": comments_disabled_globally_flag,
    }
    return context


def selected_settings(request):
    # return the version value as a dictionary
    # you may add other values here as well
    return {
        "FULL_VERSION": settings.FULL_VERSION,
    }
