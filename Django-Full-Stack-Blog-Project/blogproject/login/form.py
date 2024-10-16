from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser



class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=15)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["username", "email" ,"phone" ,"password1", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            custom_user = CustomUser(user=user, phone=self.cleaned_data['phone'])
            custom_user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)