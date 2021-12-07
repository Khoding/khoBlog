from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Role


class CustomUserAdmin(UserAdmin):
    """Admin class for CustomUserAdmin"""

    model = CustomUser

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            ("Personal Info"),
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "bio",
                    "welcome_message",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "owner",
                    "groups",
                    "roles",
                    "user_permissions",
                )
            },
        ),
        (
            ("Other"),
            {"fields": ("enable_tailwind",)},
        ),
        (
            ("Important Dates"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin class for RoleAdmin"""

    model = Role


admin.site.register(CustomUser, CustomUserAdmin)
