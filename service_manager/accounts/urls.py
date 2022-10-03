from django.urls import path

from service_manager.accounts.views import RegisterView, LoginUserView, LogoutUserView

urlpatterns = (
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
)
