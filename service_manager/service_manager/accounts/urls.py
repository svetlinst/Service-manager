from django.urls import path

from service_manager.accounts.views import RegisterView, LoginUserView, LogoutUserView, EditProfileView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = (
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
    path('password_reset/', PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
)
