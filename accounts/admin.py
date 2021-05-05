from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from comments.models import CustomComment
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (('Personal Info'), {
         'fields': ('email', 'first_name', 'last_name', 'bio', 'welcome_message',)}),
        (('Permissions'), {
         'fields': ('is_staff', 'is_superuser', 'owner', 'groups', 'user_permissions',)}),
        (('Important Dates'), {
         'fields': ('last_login', 'date_joined',)}),
    )


admin.site.register(CustomComment)

admin.site.register(CustomUser, CustomUserAdmin)
