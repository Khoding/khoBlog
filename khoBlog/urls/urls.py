"""khoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from blog.models import Post
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.urls.conf import re_path
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

from . import dev_urls

admin.site.site_header = "Khodok's Blog Admin"
admin.site.site_title = "Khodok's Blog Admin"
admin.site.index_title = "Khodok's Blog Admin"

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="Test description",
    ),
    public=False,
    permission_classes=(permissions.IsAdminUser,),
)

site_map_info_dict = {
    'queryset': Post.objects.filter(published_date__lte=timezone.now(), withdrawn=False),
}

api_patterns = [
    path('', include('khoBlogAPI.urls')),
    path('docs/', schema_view.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
]

api_patterns_v2 = [
    path('', include('blog.blogAPIurls')),
    path('docs/', schema_view.with_ui('redoc',
                                      cache_timeout=0), name='schema-redoc'),
]

api_base_patterns = [
    re_path(r'(?P<version>[v1]+)/',
            include(api_patterns)),
    re_path(r'(?P<version>[v2]+)/',
            include(api_patterns_v2)),
    path('read/', include('reading_apis_app.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', obtain_auth_token, name='obtain-token'),
]

urlpatterns = [
    # My Apps
    path('', include('blog.urls')),
    path('projects/', include('portfolio.urls')),
    path('pages/', include('pages.urls')),
    path('polls/', include('polls.urls')),
    path('todo/', include('todo.urls')),
    path('s/', include('shortener.urls')),
    path('l/', include('links.urls')),

    # Rest API
    path('api/', include(api_base_patterns)),

    # Django Admin
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # User Management
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),

    # Dev Urls
    path('dev/', include(dev_urls, namespace='dev')),

    # Markdownx
    path('markdownx/', include('markdownx.urls')),

    re_path(r'^comments/', include('comments.urls')),
    re_path(r'^comments/', include('django_comments.urls')),

    path('sitemap.xml', sitemap,
         {'sitemaps': {'blog': GenericSitemap(
             site_map_info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^robots\.txt', include('robots.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
