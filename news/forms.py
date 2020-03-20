from django import forms 
from .models import User
# class UserForm(forms.Form):
#     login = forms.CharField()
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     image = forms.CharField(widget = forms.FileInput)
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import NON_FIELD_ERRORS
from news.models import News
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

#форма которая используется при регистрации
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username',)
#форма которая используется в интерфейсе администратора
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"formBtn", "placeholder":"Имя"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"formBtn", "placeholder":"Email"}))
    password = forms.CharField(widget=forms.TextInput(attrs={"class":"formBtn", "placeholder":"Пароль", "type":"password"}))


    class Meta:
        model = User
        fields = ('username','email','password')
        error_messages = {
        NON_FIELD_ERRORS: {
            'phone': "dsa",
        }
    }

    def save(self, commit=True):
        """Переопределение метода save"""
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user 

class ProfileEditForm(forms.ModelForm):
    addres = forms.CharField(widget=forms.Textarea(attrs={'class':'contacts-textarea'}))
    phone = forms.CharField(error_messages={'phone': 'Please enter your name'})
    class Meta:
        model = User
        fields = { 'email', 'gender', 'phone', 'organization', 'skype', 'addres','patronymic','last_name','first_name','dateBirth'}
     
    error_messages = {
        NON_FIELD_ERRORS: {
            'phone': "dsa",
        }
    }

class NewsAddForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = {'title', 'small_text','text','image' }




# class MessageSubmitForm(forms.ModelForm):
#     class Meta:
#         model = Message



#cleaned_date - просто возвращает объект из объекта формы (проверенный объект)
#commit - вносить или не вносить изменения в бд