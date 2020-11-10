from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from allauth.socialaccount.views import ConnectionsView, DisconnectForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account_login')
    template_name = 'account/signup.html'


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        context['users'] = CustomUser.objects.all()
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

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Password'
        return context


class ConnectionsEditView(ConnectionsView):
    form_class = DisconnectForm
    template_name = 'account/connections.html'
