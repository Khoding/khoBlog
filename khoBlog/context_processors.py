from django.conf import settings
from django.urls.base import reverse
from django.utils import timezone


def context(request):
    debug_flag = settings.DEBUG
    comments_disabled_globally_flag = settings.COMMENTS_DISABLED_GLOBALLY
    enable_tailwind_flag = settings.ENABLE_TAILWIND
    context = {
        "CANONICAL_PATH": request.build_absolute_uri(request.path_info),
        "debug_flag": debug_flag,
        "now": timezone.now(),
        "description": "Welcome to my website, it's a blog, a portfolio, a personal playground, and too much time is dedicated to it.",
        "app_title": "Blog",
        "app_direct_link": reverse("blog:post_list"),
        "show_featured": False,
        "comments_disabled_globally_flag": comments_disabled_globally_flag,
        "enable_tailwind_flag": enable_tailwind_flag,
        "content_type": "post",
    }
    return context


def selected_settings(request):
    # return the version value as a dictionary
    # you may add other values here as well
    return {
        "APP_VERSION_NUMBER": settings.APP_VERSION_NUMBER,
        "APP_VERSION_NAME": settings.APP_VERSION_NAME,
    }


def base_site_template(request):
    # Here goes your conditions to select proper base template, for example
    # by checking request.user permissions or some other logic.
    BASE_SITE_TEMPLATE = "tailwind/base.html"
    return {"BASE_SITE_TEMPLATE": BASE_SITE_TEMPLATE}
