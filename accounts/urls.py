from django.conf.urls import include
from django.urls import path

from .views import (ConnectionsEditView, PasswordsChangeView, ProfileView,
                    SignUpView, UserEditView)

app_name = "accounts"
extra_patterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('edit/', UserEditView.as_view(), name='edit_profile'),
    path('edit_connections/', ConnectionsEditView.as_view(),
         name='edit_connections'),
    path('password/',
         PasswordsChangeView.as_view(), name='edit_password'),
]

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', include(extra_patterns)),
    path('profile/<slug:slug>/', include(extra_patterns))
]
