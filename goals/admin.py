from django.contrib import admin
from .models import GoalType, GoalResultType, GoalsBacklog


@admin.register(GoalType)
class GoalTypeAdmin(admin.ModelAdmin):
    """Админка для типов целей"""
    list_display = ('type_name', 'createdat', 'modifiedat')
    search_fields = ('type_name',)
    readonly_fields = ('createdat', 'modifiedat')


@admin.register(GoalResultType)
class GoalResultTypeAdmin(admin.ModelAdmin):
    """Админка для типов результатов целей"""
    list_display = ('type_name', 'createdat', 'modifiedat')
    search_fields = ('type_name',)
    readonly_fields = ('createdat', 'modifiedat')


class GoalsBacklogInline(admin.TabularInline):
    """Инлайн для целей в админке пользователя"""
    model = GoalsBacklog
    extra = 0
    fields = ('goal_name', 'goal_type', 'priority_weight', 'visibleforothers')
    readonly_fields = ('createdat',)


@admin.register(GoalsBacklog)
class GoalsBacklogAdmin(admin.ModelAdmin):
    """Админка для целей в бэклоге"""
    list_display = ('goal_name', 'nsuser', 'goal_type', 'priority_weight', 'visibleforothers', 'createdat')
    list_filter = ('goal_type', 'goal_result_type', 'visibleforothers', 'createdat')
    search_fields = ('goal_name', 'goal_reason', 'nsuser__userlogin')
    readonly_fields = ('createdat', 'modifiedat')
    fieldsets = (
        (None, {
            'fields': ('goal_name', 'nsuser', 'goal_type', 'goal_result_type')
        }),
        ('Детали цели', {
            'fields': ('goal_reason', 'priority_weight', 'visibleforothers')
        }),
        ('Служебные поля', {
            'fields': ('createdat', 'modifiedat'),
            'classes': ('collapse',)
        }),
    )