from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm)

from polls.utils import AuthFormMixin

from users.models import MyUser


class SignUpForm(AuthFormMixin, UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2')


class SignInForm(AuthFormMixin, AuthenticationForm):
    class Meta:
        model = MyUser
