from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import django.views.generic as views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views, login

from service_manager import settings
from service_manager.accounts.forms import RegisterForm, LoginForm, EditProfileForm, PasswordResetForm
from service_manager.accounts.models import Profile


class RegisterView(views.CreateView):
    form_class = RegisterForm
    template_name = 'register_user.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserView(auth_views.LoginView):
    template_name = 'login_user.html'
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        return reverse_lazy('index')


class LogoutUserView(auth_views.LogoutView):
    pass


class EditProfileView(LoginRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('index')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'password/password_reset.html'
    form_class = PasswordResetForm
    from_email = settings.EMAIL_HOST_USER
    success_url = reverse_lazy('index')
    subject_template_name = 'password/password_reset_subject.txt'
    email_template_name = 'password/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password/password_reset_complete.html'
