from django.urls import path
from django.urls.conf import include

from .views import (ResourceCreateView, ResourceDeleteView, ResourceDetailView,
                    ResourceUpdateView)

actions_extra_patterns = [
    path('', ResourceDetailView.as_view(), name='resource_detail'),
    path('edit/', ResourceUpdateView.as_view(), name='resource_update'),
    path('delete/', ResourceDeleteView.as_view(), name='resource_delete')
]

urlpatterns = [
    path('add/', ResourceCreateView.as_view(), name='resource_create'),
    path('<pk>/', include(actions_extra_patterns)),
]
