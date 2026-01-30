from django import forms
from django.contrib .auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from .models import NSUser

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'autocomplete': 'new-password'
        }),
        help_text="Введите надежный пароль"

    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password'
        }),
        help_text="Для подтверждения введите пароль ещё раз"
    )

    class Meta:
        model = NSUser
        fields = ('userlogin', 'useremail', 'userphone')
        widgets = {
            'userlogin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Придумайте логин',
                'autocomplete': 'off'
            }),
            'useremail': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com',
                'autocomplete': 'off'
            }),
            'userphone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX',
                'autocomplete': 'off'
            }),
        }
        labels = {
            'userlogin': 'Логин',
            'useremail': 'Электронная почта',
            'userphone': 'Телефон (необязательно)',
        }
        help_texts = {
            'userlogin': 'Уникальный логин пользователя (макс. 30 символов)',
            'useremail': 'Уникальный email пользователя',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настройка crispy-forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('userlogin', css_class='form-control-lg'),
            Field('useremail', css_class='form-control-lg'),
            Field('userphone', css_class='form-control-lg'),
            Field('password1', css_class='form-control-lg'),
            Field('password2', css_class='form-control-lg'),
            Submit('submit', 'Зарегистрироваться', css_class='btn btn-primary btn-lg w-100 mt-3')
        )

    def clean_password2(self):
        # Проверка совпадения паролей
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
          Field('username',
                  placeholder="Введите логин",
                  css_class="form-control-lg",
                  label="Логин"),
            Field('password',
                  placeholder="Введите пароль",
                  css_class="form-control-lg",
                  label="Пароль"),
            Submit('submit', 'Войти',
                   css_class='btn btn-primary btn-lg w-100 mt-3')
        )

    def clean(self):
        userlogin = self.cleaned_data.get('userlogin')
        password = self.cleaned_data.get('password')

        if userlogin and password:
            # Проверяем существование пользователя
            try:
                user = NSUser.objects.get(userlogin=userlogin)
                if user.check_password(password):
                    # Проверяем верификацию email
                    if hasattr(user, 'profile') and not user.profile.email_verified:
                        from .utils import send_verification_email
                        # Можно отправить ссылку повторно
                        raise ValidationError(
                            'Email не подтвержден. Проверьте вашу почту для получения ссылки подтверждения. '
                            'Если вы не получили письмо, свяжитесь с администратором.'
                        )
            except NSUser.DoesNotExist:
                raise ValidationError(
                    'Пользователь с таким логином не существует, либо некорректный пароль'
                )

        return super().clean()


class ResendVerificationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )