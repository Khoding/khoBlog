from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from allauth.account.views import (
    EmailView,
    PasswordChangeView,
    PasswordResetDoneView,
    PasswordResetFromKeyDoneView,
    PasswordResetFromKeyView,
    PasswordResetView,
    PasswordSetView,
    SignupView,
)
from allauth.socialaccount.views import ConnectionsView, DisconnectForm

from khoBlog.utils.superuser_required import superuser_required, superuser_required_ignore_secure_mode

from .forms import ToggleSecureModeStatusForm, CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class SignUpView(SignupView):
    """SignUpView Class"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("account_login")
    template_name = "account/signup.html"

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Sign up"
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    """ProfileView Class"""

    model = CustomUser
    template_name = "account/profile.html"
    view_as = "self"

    def get(self, request, *args, **kwargs):
        """Get"""
        if (
            request.GET.get("view_as") is None
            or request.GET.get("view_as") == ""
            or request.GET.get("view_as") == "self"
        ):
            self.view_as = "self"
        else:
            self.view_as = "guest"
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile • " + str(self.model.objects.get(username=kwargs["object"]))
        context["description"] = str(self.model.objects.get(username=kwargs["object"]).bio)
        context["view_as"] = self.view_as
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    """UserEditView Class"""

    form_class = CustomUserChangeForm
    template_name = "account/edit_profile.html"
    model = CustomUser

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Profile"
        return context


class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    """CustomPasswordSetView Class"""

    template_name = "account/password_set.html"
    success_url = reverse_lazy("account_login")
    model = CustomUser

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Set Password"
        return context


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """CustomPasswordChangeView Class"""

    template_name = "account/password_change.html"
    success_url = reverse_lazy("account_login")
    model = CustomUser

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Password"
        return context


class CustomPasswordResetView(PasswordResetView):
    """CustomPasswordResetView Class"""

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Reset Password"
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """CustomPasswordResetDoneView Class"""

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Password requested"
        return context


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    """CustomPasswordResetFromKeyView Class"""

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Set a new password"
        return context


class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    """CustomPasswordResetFromKeyDoneView Class"""

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "New password set"
        return context


class ConnectionsEditView(LoginRequiredMixin, ConnectionsView):
    """ConnectionsEditView Class"""

    form_class = DisconnectForm
    template_name = "account/connections.html"
    model = CustomUser

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Connections"
        return context


class EmailEditView(LoginRequiredMixin, EmailView):
    """EmailEditView Class"""

    model = CustomUser

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Email"
        return context


@superuser_required()
class UserListView(ListView):
    """UserListView Class"""

    model = CustomUser
    template_name = "account/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        """Get queryset"""
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "User list"
        return context


@superuser_required_ignore_secure_mode()
class ToggleSecureModeStatusUpdateView(UpdateView):
    """ToggleSecureModeStatusUpdateView UpdateView"""

    model = CustomUser
    form_class = ToggleSecureModeStatusForm
    template_name = "account/toggle_secure_mode_status.html"

    def form_valid(self, form):
        """Form valid"""
        user = get_object_or_404(self.model, pk=form.instance.pk)
        if user.secure_mode:
            form.instance.secure_mode = False
        else:
            form.instance.secure_mode = True
        form.instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Change Secure Mode Status"
        return context
