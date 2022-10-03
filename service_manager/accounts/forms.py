import django.contrib.auth.forms as auth_forms
from django.contrib.auth import authenticate, get_user_model

from service_manager.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class RegisterForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)


class LoginForm(BootstrapFormMixin, auth_forms.AuthenticationForm):
    pass


class LogoutForm:
    pass
