"""khoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/latest/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import index, sitemap
from django.urls import include, path
from django.urls.conf import re_path

from khoBlog.views import ServiceWorkerView, offline

try:
    if settings.DEBUG and settings.ENABLE_DEBUG_TOOLBAR:
        import debug_toolbar  # noqa
except ImportError:
    pass

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

from blog.sitemap import CategorySitemap, PostSitemap, SeriesSitemap
from pages.sitemap import PageSitemap

from . import dev_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v3",
        description="API v3",
    ),
    public=False,
    permission_classes=(permissions.DjangoModelPermissionsOrAnonReadOnly,),
)

sitemaps = {
    "blog": PostSitemap,
    "category": CategorySitemap,
    "series": SeriesSitemap,
    "pages": PageSitemap,
}

api_patterns = [
    path("", include("blog.blogAPIurls")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

api_base_patterns = [
    path("read/", include("reading_apis_app.urls")),
    re_path(r"(?P<version>v[3]{1})/", include(api_patterns)),
    re_path(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("token/", obtain_auth_token, name="obtain-token"),
]

urlpatterns = (
    [
        # My Apps
        path("", include("blog.urls")),
        path("projects/", include("portfolio.urls")),
        path("pages/", include("pages.urls")),
        path("polls/", include("polls.urls")),
        path("todo/", include("todo.urls")),
        path("tags/", include("custom_taggit.urls")),
        path("quote/", include("quotes.urls")),
        path("s/", include("shortener.urls")),
        path("l/", include("links.urls")),
        # Rest API
        path("api/", include(api_base_patterns)),
        # Django Admin
        path("admin/docs/", include("django.contrib.admindocs.urls")),
        path("admin/", admin.site.urls),
        # User Management
        path("accounts/", include("accounts.urls")),
        path("accounts/", include("allauth.urls")),
        path("captcha/", include("captcha.urls")),
        # Markdownx, taggit
        path("markdownx/", include("markdownx.urls")),
        re_path(r"^taggit/", include("taggit_selectize.urls")),
        # Comments
        re_path(r"^comments/", include("comments.urls")),
        re_path(r"^comments/", include("django_comments.urls")),
        re_path(r"^comments/", include("django_comments_xtd.urls")),
        # PWA
        path(
            "sw.js",
            ServiceWorkerView.as_view(content_type="application/javascript"),
            name="sw.js",
        ),
        path("offline/", offline, name="offline"),
        # Sitemaps
        path("sitemap.xml", index, {"sitemaps": sitemaps}),
        path(
            "sitemap-<section>.xml",
            sitemap,
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
        # Tailwind
        path("__reload__/", include("django_browser_reload.urls")),
        # Misc
        re_path(r"^robots\.txt", include("robots.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    urlpatterns += [
        # Dev Urls
        path("dev/", include(dev_urls, namespace="dev")),
    ]

if settings.DEBUG and settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
