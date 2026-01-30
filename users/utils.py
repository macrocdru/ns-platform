from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


def send_verification_email(user, request):
    """Отправка email с ссылкой верификации"""
    from .models import UserProfile

    profile, created = UserProfile.objects.get_or_create(user=user)
    token = profile.generate_verification_token()

    # Формируем абсолютный URL
    verification_url = request.build_absolute_uri(
        reverse('users:verify_email', kwargs={'token': token})
    )

    subject = 'Подтверждение email на платформе NS Platform'
    message = f'''
    Здравствуйте, {user.username}! 

    Для завершения регистрации и подтверждения вашего email адреса, 
    пожалуйста, перейдите по следующей ссылке:

    {verification_url}

    Ссылка действительна в течение 24 часов.

    Если вы не регистрировались на NS Platform, пожалуйста, проигнорируйте это письмо.

    С уважением,
    Команда NS Platform'''
    

    # TODO: Переделать на html письмо
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.useremail],
        fail_silently=False,
    )

    return True