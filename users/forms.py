from django import forms
from django.contrib .auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from .models import NSUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = NSUser
        fields = ['userlogin', 'useremail', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NSUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.useremail = self.cleaned_data['useremail']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    userlogin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
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