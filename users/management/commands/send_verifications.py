from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Q
from users.utils import send_verification_email


class Command(BaseCommand):
    help = 'Отправляет письма для подтверждения email незавершенным пользователям'

    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Отправить всем пользователям')
        parser.add_argument('--emails', type=str, help='Список email через запятую')

    def handle(self, *args, **options):
        users = User.objects.all()

        if options['emails']:
            emails = [email.strip() for email in options['emails'].split(',')]
            users = users.filter(email__in=emails)

        if not options['all'] and not options['emails']:
            # По умолчанию только незавершенные
            users = users.filter(
                Q(profile__email_verified=False) | Q(profile__isnull=True)
            )

        count = 0
        for user in users:
            try:
                send_verification_email(user, None)
                self.stdout.write(
                    self.style.SUCCESS(f'Отправлено для {user.email}')
                )
                count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка для {user.email}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Всего отправлено: {count} писем')
        )