from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, email_verification, password_recovery, \
    UserListView, user_toggle_activity

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('verification/', email_verification, name='verification'),
    path('recovery/', password_recovery, name='recovery'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('user/activity/<int:pk>/', user_toggle_activity, name='user_activity'),
]
