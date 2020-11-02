from django.urls import path
from .views import SignUpView, ProfileView, UserEditView, PasswordsChangeView, ConnectionsEditView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('edit_connections/', ConnectionsEditView.as_view(), name='edit_connections'),
    path('password/', PasswordsChangeView.as_view()),
]
