from allauth.socialaccount.views import ConnectionsView, DisconnectForm
from blog.models import Comment
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
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
        if request.GET.get("view_as") is None or request.GET.get("view_as") == "" or request.GET.get("view_as") == "self":
            self.view_as = 'self'
        else:
            self.view_as = 'guest'
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile • ' + \
            str(self.model.objects.get(username=kwargs['object']))
        context['description'] = str(
            self.model.objects.get(username=kwargs['object']).bio)
        context['users'] = CustomUser.objects.all()
        context['comments'] = Comment.objects.filter(
            author_logged=kwargs['object'])
        context['view_as'] = self.view_as
        return context


class UserEditView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'account/edit_profile.html'

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Profile'
        return context


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'
    success_url = reverse_lazy('account_login')

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Password'
        return context


class ConnectionsEditView(ConnectionsView):
    form_class = DisconnectForm
    template_name = 'account/connections.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Connections'
        return context
