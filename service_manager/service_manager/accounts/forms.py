import django.contrib.auth.forms as auth_forms
from django.contrib.auth import authenticate, get_user_model
import django.forms as forms

from service_manager.accounts.models import Profile
from service_manager.accounts.tasks import send_password_reset_email_async
from service_manager.core.forms import BootstrapFormMixin
from service_manager.core.validators import validate_digits_only
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

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

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

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
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    pass


class LogoutForm:
    pass


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number')


class PasswordResetForm(BootstrapFormMixin, auth_forms.PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id

        send_password_reset_email_async.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context, from_email=from_email, to_email=to_email,
            html_email_template_name=html_email_template_name
        )


class PasswordResetSetPasswordForm(BootstrapFormMixin, auth_forms.SetPasswordForm):
    pass
