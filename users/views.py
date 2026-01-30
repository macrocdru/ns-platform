from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as AuthLoginView
from .forms import UserRegistrationForm,LoginForm, ResendVerificationForm
from .utils import send_verification_email
from .models import UserProfile

def home(request):
    return render(request, 'home.html')


class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance

        # Отправляем email для верификации
        send_verification_email(user, self.request)

        messages.success(
            self.request,
            'Регистрация успешна! '
            'На ваш email отправлена ссылка для подтверждения. '
            'После подтверждения вы сможете войти в систему.'
        )
        return response


class LoginView(AuthLoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Проверьте правильность данных.')
        return super().form_invalid(form)


def verify_email(request, token):
    """Подтверждение email по токену"""
    try:
        profile = UserProfile.objects.get(verification_token=token)

        if not profile.is_token_valid():
            messages.error(
                request,
                'Срок действия ссылки истек. '
                'Запросите новую ссылку для подтверждения.'
            )
            return redirect('users:resend_verification')

        # Активируем пользователя
        profile.email_verified = True
        profile.verification_token = None
        profile.token_created_at = None
        profile.save()

        messages.success(
            request,
            'Email успешно подтвержден! Теперь вы можете войти в систему.'
        )
        return redirect('users:log  in')

    except UserProfile.DoesNotExist:
        messages.error(request, 'Неверная или устаревшая ссылка подтверждения.')
        return redirect('main:home')


class ResendVerificationView(FormView):
    form_class = ResendVerificationForm
    template_name = 'users/resend_verification.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        try:
            user = User.objects.get(email=email)

            if hasattr(user, 'profile'):
                if user.profile.email_verified:
                    messages.info(self.request, 'Ваш email уже подтвержден.')
                    return redirect('users:login')

                # Отправляем новую ссылку
                send_verification_email(user, self.request)

                messages.success(
                    self.request,
                    'Новая ссылка для подтверждения отправлена на ваш email. '
                    'Ссылка действительна 24 часа.'
                )
            else:
                messages.error(self.request, 'Профиль пользователя не найден.')

        except User.DoesNotExist:
            messages.error(self.request, 'Пользователь с таким email не найден.')

        return super().form_valid(form)


@login_required
def profile(request):
    """Профиль пользователя"""
    return render(request, 'users/profile.html', {
        'user': request.user
    })