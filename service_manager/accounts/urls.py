from django.urls import path

from service_manager.accounts.views import RegisterView, LoginUserView, LogoutUserView, EditProfileView

urlpatterns = (
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
)
