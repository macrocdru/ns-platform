from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NSUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = NSUser
        fields = ['userlogin', 'useremail', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.useremail = self.cleaned_data['useremail']
        if commit:
            user.save()
        return user
