from django.conf.urls import include
from django.urls import path
from django.urls.conf import re_path

from .views import (
    ConnectionsEditView,
    CustomPasswordChangeView,
    CustomPasswordResetDoneView,
    CustomPasswordResetFromKeyDoneView,
    CustomPasswordResetFromKeyView,
    CustomPasswordResetView,
    CustomPasswordSetView,
    EmailEditView,
    ProfileView,
    SignUpView,
    UserEditView,
)

app_name = "accounts"
password_reset_extra_patterns = [
    path("", CustomPasswordResetView.as_view(), name="reset_password"),
    path(
        "done/",
        CustomPasswordResetDoneView.as_view(),
        name="account_reset_password_done",
    ),
    re_path(
        r"^key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        CustomPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path(
        "key/done/",
        CustomPasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done",
    ),
]

password_extra_patterns = [
    path("set/", CustomPasswordSetView.as_view(), name="set_password"),
    path("change/", CustomPasswordChangeView.as_view(), name="edit_password"),
    path("reset/", include(password_reset_extra_patterns)),
]

extra_patterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("edit/", UserEditView.as_view(), name="edit_profile"),
]

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/<int:pk>/", include(extra_patterns)),
    path("profile/<slug:slug>/", include(extra_patterns)),
    path("password/", include(password_extra_patterns)),
    path("connections/", ConnectionsEditView.as_view(), name="connections"),
    path("email/", EmailEditView.as_view(), name="email"),
]
