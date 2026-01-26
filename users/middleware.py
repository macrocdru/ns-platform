# users/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Исключаем определенные пути из проверки
        excluded_paths = [
            reverse('users:logout'),
            reverse('users:resend_verification'),
           # reverse('users:verify_email'),
            reverse('users:login'),
            reverse('users:register'),
            reverse('admin:login'),
            reverse('admin:index'),
        ]

        if request.user.is_authenticated and not request.path.startswith('/admin/'):
            # Проверяем, подтвержден ли email
            if hasattr(request.user, 'profile') and not request.user.profile.email_verified:
                if request.path not in excluded_paths:
                    messages.warning(
                        request,
                        'Пожалуйста, подтвердите ваш email для полного доступа к системе.'
                    )
                    return redirect('users:resend_verification')

        return None