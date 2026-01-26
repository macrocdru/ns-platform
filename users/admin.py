from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import NSUser, NSRole,UserProfile

from .utils import send_verification_email

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


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'
    readonly_fields = ('email_verified', 'token_created_at')

    def has_add_permission(self, request, obj=None):
        return False


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    actions = ['resend_verification_email']

    def save_model(self, request, obj, form, change):
        """При создании пользователя отправляем email для верификации"""
        is_new = not change

        super().save_model(request, obj, form, change)

        if is_new:
            # Для нового пользователя отправляем письмо с верификацией
            try:
                send_verification_email(obj, request)
                self.message_user(
                    request,
                    f"Письмо для подтверждения email отправлено на {obj.email}"
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Ошибка отправки письма: {str(e)}",
                    level='ERROR'
                )

    def resend_verification_email(self, request, queryset):
        """Действие для повторной отправки email верификации"""
        for user in queryset:
            if hasattr(user, 'profile') and not user.profile.email_verified:
                try:
                    send_verification_email(user, request)
                    self.message_user(
                        request,
                        f"Письмо отправлено на {user.email}"
                    )
                except Exception as e:
                    self.message_user(
                        request,
                        f"Ошибка отправки для {user.email}: {str(e)}",
                        level='ERROR'
                    )
        self.message_user(request, f"Письма отправлены выбранным пользователям")

    resend_verification_email.short_description = "Отправить письмо для подтверждения email"