from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from datetime import timedelta



class NSUserManager(BaseUserManager):
    """Менеджер для модели NSUser"""

    def create_user(self, userlogin, useremail, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с указанным логином, email и паролем.
        """
        if not userlogin:
            raise ValueError('Логин пользователя должен быть указан')
        if not useremail:
            raise ValueError('Email пользователя должен быть указан')

        useremail = self.normalize_email(useremail)
        user = self.model(
            userlogin=userlogin,
            useremail=useremail,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userlogin, useremail, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(userlogin, useremail, password, **extra_fields)


class NSUser(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя системы (таблица nsusers)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    username = models.CharField(
        _('Имя пользователя'),
        max_length=30,
        blank=True,
        null=True
    )
    userlogin = models.CharField(
        _('Логин'),
        max_length=30,
        unique=True,
        help_text=_('Уникальный логин пользователя')
    )
    useremail = models.EmailField(
        _('Электронная почта'),
        max_length=250,
        unique=True,
        help_text=_('Уникальный email пользователя')
    )
    userphone = models.CharField(
        _('Телефон'),
        max_length=20,
        blank=True,
        null=True,
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

    # Поля для Django auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = NSUserManager()

    USERNAME_FIELD = 'userlogin'
    REQUIRED_FIELDS = ['useremail']

    class Meta:
        db_table = 'nsusers'
        verbose_name = _('Пользователь системы')
        verbose_name_plural = _('Пользователи системы')
        ordering = ['userlogin']

    def __str__(self):
        return f"{self.userlogin} ({self.useremail})"

    def get_full_name(self):
        return self.username or self.userlogin
    def get_short_name(self):
        return self.userlogin

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    user = models.ForeignKey(
        NSUser,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='profile')
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(null=True, blank=True)
    verification_sent_at = models.DateTimeField(null=True, blank=True)

    def generate_verification_token(self):
        """Генерация нового токена верификации"""
        self.verification_token = uuid.uuid4().hex
        self.token_created_at = timezone.now()
        self.save()
        return self.verification_token

    def is_token_valid(self):
        """Проверка валидности токена (24 часа)"""
        if not self.token_created_at or not self.verification_token:
            return False
        return timezone.now() < self.token_created_at + timedelta(hours=24)

    def __str__(self):
        return f"{self.user.username} - {'Verified' if self.email_verified else 'Not Verified'}"


@receiver(post_save, sender=NSUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=NSUser)
def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

class NSRole(models.Model):
    """Модель ролей системы (таблица nsroles)"""
    id = models.AutoField(primary_key=True, verbose_name=_('ID'))
    rolename = models.CharField(
        _('Имя роли'),
        max_length=16,
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
        db_table = 'nsroles'
        verbose_name = _('Роль системы')
        verbose_name_plural = _('Роли системы')
        ordering = ['id']

    def __str__(self):
        return self.rolename