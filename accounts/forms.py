from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from news.models import User
class MyAuthenticationForm(AuthenticationForm):
    password = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', "class":"formBtn", "placeholder":"Пароль"}),
    )
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, "class":"formBtn", "placeholder":"Логин"}))
   
