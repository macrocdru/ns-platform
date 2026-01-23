from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import NSUser, NSRole


class NSUserAdmin(UserAdmin):
    """Админка для пользователя NS"""
    list_display = ('userlogin', 'useremail', 'username', 'userphone', 'is_active', 'createdat')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'createdat')
    search_fields = ('userlogin', 'useremail', 'username', 'userphone')
    ordering = ('-createdat',)

    fieldsets = (
        (None, {'fields': ('userlogin', 'password')}),
        (_('Personal info'), {'fields': ('username', 'useremail', 'userphone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'createdat', 'modifiedat')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('userlogin', 'useremail', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('createdat', 'modifiedat')


class NSRoleAdmin(admin.ModelAdmin):
    """Админка для ролей системы"""
    list_display = ('rolename', 'createdat', 'modifiedat')
    search_fields = ('rolename',)


admin.site.register(NSUser, NSUserAdmin)
admin.site.register(NSRole, NSRoleAdmin)