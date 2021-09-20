from allauth.account.views import (EmailView, PasswordChangeView,
                                   PasswordResetDoneView,
                                   PasswordResetFromKeyDoneView,
                                   PasswordResetFromKeyView, PasswordResetView,
                                   PasswordSetView, SignupView)
from allauth.socialaccount.views import ConnectionsView, DisconnectForm
from blog.models import Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class SignUpView(SignupView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account_login')
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign up'
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'account/profile.html'
    view_as = 'self'

    def get(self, request, *args, **kwargs):
        if request.GET.get("view_as") is None or request.GET.get("view_as") == "" or request.GET.get(
                "view_as") == "self":
            self.view_as = 'self'
        else:
            self.view_as = 'guest'
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile • ' + \
                           str(self.model.objects.get(
                               username=kwargs['object']))
        context['description'] = str(
            self.model.objects.get(username=kwargs['object']).bio)
        context['users'] = CustomUser.objects.all()
        context['comments'] = Comment.objects.filter(
            author_logged=kwargs['object'])
        context['view_as'] = self.view_as
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'account/edit_profile.html'
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Profile'
        return context


class CustomPasswordSetView(LoginRequiredMixin, PasswordSetView):
    template_name = 'account/password_set.html'
    success_url = reverse_lazy('account_login')
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Set Password'
        return context


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('account_login')
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Password'
        return context


class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reset Password'
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password requested'
        return context


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Set a new password'
        return context


class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New password set'
        return context


class ConnectionsEditView(LoginRequiredMixin, ConnectionsView):
    form_class = DisconnectForm
    template_name = 'account/connections.html'
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Connections'
        return context


class EmailEditView(LoginRequiredMixin, EmailView):
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Email'
        return context
