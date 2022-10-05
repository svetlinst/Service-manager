import django.contrib.auth.forms as auth_forms
from django.contrib.auth import authenticate, get_user_model
import django.forms as forms

from service_manager.accounts.models import Profile
from service_manager.core.forms import BootstrapFormMixin
from service_manager.core.validators import validate_digits_only

UserModel = get_user_model()


class RegisterForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 20
    PHONE_NUMBER_MAX_LENGTH = 20

    first_name = forms.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    )

    last_name = forms.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
    )

    phone_number = forms.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        validators=[validate_digits_only, ]
    )

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name', 'phone_number',)

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            app_user=user,
        )

        if commit:
            profile.save()

        return user


class LoginForm(BootstrapFormMixin, auth_forms.AuthenticationForm):
    pass


class LogoutForm:
    pass


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number')

