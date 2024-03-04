from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'role'
    )
    list_editable = (
        'role',
    )


UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role')}),
)
