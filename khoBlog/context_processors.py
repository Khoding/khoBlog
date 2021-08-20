from django.conf import settings
from django.urls.base import reverse
from django.utils import timezone


def context(request):
    debug_flag = settings.DEBUG
    context = {
        'CANONICAL_PATH': request.build_absolute_uri(request.path_info),
        'debug_flag': debug_flag,
        'search_url': reverse('blog:search_results'),
        'search_title': "Search in Everything",
        'now': timezone.now(),
        'description': "Khodok's Blog is Khodok's Main Website, you can find a lot of useless stuff that you'll never care about here. Enjoy your stay :D",
        'app_title': 'Blog',
    }

    return context


def selected_settings(request):
    # return the version value as a dictionary
    # you may add other values here as well
    return {'APP_VERSION_NUMBER': settings.APP_VERSION_NUMBER, 'APP_VERSION_NAME': settings.APP_VERSION_NAME}
