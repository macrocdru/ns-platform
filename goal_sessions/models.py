from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import NSUser, NSRole
from goals.models import GoalsBacklog


class SessionType(models.Model):
    """Модель типов сессий (таблица session_type)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    type_name = models.CharField(
        _('Название типа сессии'),
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
        db_table = 'session_type'
        verbose_name = _('Тип сессии')
        verbose_name_plural = _('Типы сессий')
        ordering = ['id']

    def __str__(self):
        return self.type_name


class SessionStatus(models.Model):
    """Модель статусов сессий (таблица session_status)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    type_name = models.CharField(
        _('Название статуса сессии'),
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
        db_table = 'session_status'
        verbose_name = _('Статус сессии')
        verbose_name_plural = _('Статусы сессий')
        ordering = ['id']

    def __str__(self):
        return self.type_name


class NSSession(models.Model):
    """Модель сессий целеполагания (таблица nssessions)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    session_status = models.ForeignKey(
        SessionStatus,
        on_delete=models.RESTRICT,
        db_column='session_status_id',
        verbose_name=_('Статус сессии')
    )
    session_type = models.ForeignKey(
        SessionType,
        on_delete=models.RESTRICT,
        db_column='session_type_id',
        verbose_name=_('Тип сессии')
    )
    start_date = models.DateField(
        _('Дата начала')
    )
    stop_date = models.DateField(
        _('Дата окончания')
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
        db_table = 'nssessions'
        verbose_name = _('Сессия целеполагания')
        verbose_name_plural = _('Сессии целеполагания')
        ordering = ['id']

    def __str__(self):
        return f"Сессия {self.id} ({self.start_date} - {self.stop_date})"

    @property
    def duration_days(self):
        """Количество дней сессии"""
        if self.stop_date and self.start_date:
            return (self.stop_date - self.start_date).days
        return 0

class SessionGoal(models.Model):
    """Модель целей в сессии (таблица session_goals)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    nssession = models.ForeignKey(
        NSSession,
        on_delete=models.RESTRICT,
        db_column='nssession_id',
        related_name='session_goals',
        verbose_name=_('Сессия')
    )
    goal = models.ForeignKey(
        GoalsBacklog,
        on_delete=models.RESTRICT,
        db_column='goal_id',
        verbose_name=_('Цель')
    )
    current_weight = models.IntegerField(
        _('Текущий вес'),
        help_text=_('Текущий вес цели в сессии')
    )
    goal_plan = models.CharField(
        _('Краткий план достижения'),
        max_length=1024
    )
    goal_steps = models.CharField(
        _('Что сделано для достижения цели'),
        max_length=1024
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
        db_table = 'session_goals'
        verbose_name = _('Цель в сессии')
        verbose_name_plural = _('Цели в сессии')
        ordering = ['id']

    def __str__(self):
        return f"Цель '{self.goal.goal_name}' в сессии {self.nssession.id}"


class SUR(models.Model):
    """Модель участников сессии и их ролей (таблица sur)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    nsuser = models.ForeignKey(
        NSUser,
        on_delete=models.RESTRICT,
        db_column='nsuser_id',
        verbose_name=_('Пользователь')
    )
    nsrole = models.ForeignKey(
        NSRole,
        on_delete=models.RESTRICT,
        db_column='nsrole_id',
        verbose_name=_('Роль')
    )
    nssession = models.ForeignKey(
        NSSession,
        on_delete=models.RESTRICT,
        db_column='nssession_id',
        related_name='participants',
        verbose_name=_('Сессия')
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
        db_table = 'sur'
        verbose_name = _('Участник сессии с ролью')
        verbose_name_plural = _('Участники сессий с ролями')
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['nsuser', 'nssession', 'nsrole'],
                name='unique_user_session_role'
            )
        ]

    def __str__(self):
        return f"{self.nsuser.userlogin} - {self.nsrole.rolename} в сессии {self.nssession.id}"


class GoalWeightHistory(models.Model):
    """История изменения веса цели (таблица goal_weight_history)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    nssession = models.ForeignKey(
        NSSession,
        on_delete=models.RESTRICT,
        db_column='nssession_id',
        related_name='weight_history',
        verbose_name=_('Сессия')
    )
    goal_weight = models.IntegerField(
        _('Вес цели')
    )
    change_reason = models.CharField(
        _('Причина изменения'),
        max_length=250
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
        db_table = 'goal_weight_history'
        verbose_name = _('История веса цели')
        verbose_name_plural = _('История весов целей')
        ordering = ['id']

    def __str__(self):
        return f"Вес: {self.goal_weight} (сессия {self.nssession.id})"

