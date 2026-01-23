from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import NSUser


class GoalType(models.Model):
    """Модель типов целей (таблица goal_type)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    type_name = models.CharField(
        _('Название типа цели'),
        max_length=30,
        unique=True
    )
    # Служебные поля с DateTimeField
    createdat = models.DateTimeField(
        _('Дата и время создания'),
        default=timezone.now,
        editable=False
    )
    modifiedat = models.DateTimeField(
        _('Дата и время последнего изменения'),
        auto_now=True
    )

    class Meta:
        db_table = 'goal_type'
        verbose_name = _('Тип цели')
        verbose_name_plural = _('Типы целей')
        ordering = ['id']

    def __str__(self):
        return self.type_name


class GoalResultType(models.Model):
    """Модель типов результатов целей (таблица goal_result_type)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    type_name = models.CharField(
        _('Название типа цели'),
        max_length=30,
        unique=True
    )
    # Служебные поля с DateTimeField
    createdat = models.DateTimeField(
        _('Дата и время создания'),
        default=timezone.now,
        editable=False
    )
    modifiedat = models.DateTimeField(
        _('Дата и время последнего изменения'),
        auto_now=True
    )

    class Meta:
        db_table = 'goal_result_type'
        verbose_name = _('Тип результата цели')
        verbose_name_plural = _('Типы результатов целей')
        ordering = ['id']

    def __str__(self):
        return self.type_name


class GoalsBacklog(models.Model):
    """Модель бэклога целей (таблица goals_backlog)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    nsuser = models.ForeignKey(
        NSUser,
        on_delete=models.RESTRICT,
        db_column='nsuser_id',
        related_name='goals',
        verbose_name=_('Пользователь')
    )
    goal_type = models.ForeignKey(
        GoalType,
        on_delete=models.RESTRICT,
        db_column='goal_type_id',
        verbose_name=_('Тип цели')
    )
    goal_result_type = models.ForeignKey(
        GoalResultType,
        on_delete=models.RESTRICT,
        db_column='goal_result_type_id',
        verbose_name=_('Тип результата цели')
    )
    goal_name = models.CharField(
        _('Имя цели'),
        max_length=30,
        unique=True
    )
    goal_reason = models.CharField(
        _('Причина возникновения цели'),
        max_length=250
    )
    visibleforothers = models.BooleanField(
        _('Видимость для других'),
        default=False,
        help_text=_('Цель может закрыта на просмотр остальным участникам сессии')
    )
    priority_weight = models.IntegerField(
        _('Вес цели'),
        help_text=_('Вес цели относительно всех других, уникален для пользователя')
    )

    # Служебные поля с DateTimeField
    createdat = models.DateTimeField(
        _('Дата и время создания'),
        default=timezone.now,
        editable=False
    )
    modifiedat = models.DateTimeField(
        _('Дата и время последнего изменения'),
        auto_now=True
    )

    class Meta:
        db_table = 'goals_backlog'
        verbose_name = _('Цель в бэклоге')
        verbose_name_plural = _('Цели в бэклоге')
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['nsuser', 'priority_weight'],
                name='unique_user_priority_weight'
            )
        ]

    def __str__(self):
        return f"{self.goal_name} (Вес: {self.priority_weight})"