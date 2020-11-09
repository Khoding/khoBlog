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
from django.urls.conf import re_path
from blog.models import Post
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.utils import timezone
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

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

info_dict = {
    'queryset': Post.objects.filter(published_date__lte=timezone.now(), private=False).order_by('-published_date'),
}

extra_patterns = [
    re_path(r'(?P<version>[v1]+)/', include('khoBlogAPI.urls')),
]

urlpatterns = [
    # My Apps
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('polls/', include('polls.urls')),
    path('todo/', include('todo.urls')),
    path('s/', include('shortener.urls')),

    # Rest API
    path('doc/', schema_view.with_ui('redoc',
                                     cache_timeout=0), name='schema-redoc'),
    path('apis/', include(extra_patterns)),


    # Django Admin
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # User management
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),

    # Markdownx
    path('markdownx/', include('markdownx.urls')),

    path('sitemap.xml', sitemap,
         {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
