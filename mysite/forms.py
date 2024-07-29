from django import forms
from mysite.models import Profile, Post


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class RegisterForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput)
    role = forms.

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            self.add_error("password_confirm", "Пароли не совпадают")
            return False
        return valid


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
