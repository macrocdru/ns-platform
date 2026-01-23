from django.contrib import admin
from .models import (
    SessionType, SessionStatus, NSSession,
    SessionGoal, SUR, GoalWeightHistory
)


@admin.register(SessionType)
class SessionTypeAdmin(admin.ModelAdmin):
    """Админка для типов сессий"""
    list_display = ('type_name', 'createdat', 'modifiedat')
    search_fields = ('type_name',)
    readonly_fields = ('createdat', 'modifiedat')


@admin.register(SessionStatus)
class SessionStatusAdmin(admin.ModelAdmin):
    """Админка для статусов сессий"""
    list_display = ('type_name', 'createdat', 'modifiedat')
    search_fields = ('type_name',)
    readonly_fields = ('createdat', 'modifiedat')


class SessionGoalInline(admin.TabularInline):
    """Инлайн для целей сессии"""
    model = SessionGoal
    extra = 1
    readonly_fields = ('createdat', 'modifiedat')


class SURInline(admin.TabularInline):
    """Инлайн для участников сессии"""
    model = SUR
    extra = 1
    readonly_fields = ('createdat', 'modifiedat')


class GoalWeightHistoryInline(admin.TabularInline):
    """Инлайн для истории весов целей"""
    model = GoalWeightHistory
    extra = 1
    readonly_fields = ('createdat', 'modifiedat')


@admin.register(NSSession)
class NSSessionAdmin(admin.ModelAdmin):
    """Админка для сессий целеполагания"""
    list_display = ('id', 'session_type', 'session_status', 'start_date', 'stop_date', 'createdat')
    list_filter = ('session_type', 'session_status', 'start_date')
    search_fields = ('id',)
    readonly_fields = ('createdat', 'modifiedat', 'duration_days')
    inlines = [SessionGoalInline, SURInline, GoalWeightHistoryInline]
    fieldsets = (
        (None, {
            'fields': ('session_type', 'session_status')
        }),
        ('Даты', {
            'fields': ('start_date', 'stop_date', 'duration_days')
        }),
        ('Служебные поля', {
            'fields': ('createdat', 'modifiedat'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SessionGoal)
class SessionGoalAdmin(admin.ModelAdmin):
    """Админка для целей в сессии"""
    list_display = ('goal', 'nssession', 'current_weight', 'createdat')
    list_filter = ('nssession__session_type', 'createdat')
    search_fields = ('goal__goal_name', 'goal_plan', 'goal_steps')
    readonly_fields = ('createdat', 'modifiedat')


@admin.register(SUR)
class SURAdmin(admin.ModelAdmin):
    """Админка для участников сессий с ролями"""
    list_display = ('nsuser', 'nsrole', 'nssession', 'createdat')
    list_filter = ('nsrole', 'nssession__session_type')
    search_fields = ('nsuser__userlogin', 'nsrole__rolename')
    readonly_fields = ('createdat', 'modifiedat')


@admin.register(GoalWeightHistory)
class GoalWeightHistoryAdmin(admin.ModelAdmin):
    """Админка для истории весов целей"""
    list_display = ('nssession', 'goal_weight', 'change_reason', 'createdat')
    list_filter = ('nssession', 'createdat')
    search_fields = ('change_reason',)
    readonly_fields = ('createdat', 'modifiedat')
