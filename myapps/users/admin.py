from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ['email', 'first_name', 'last_name', 'role']}),
    )

    fieldsets = (
        (None, {'fields': ('username',)}),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'role',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_superuser', 'user_permissions'),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


