from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserProfile, email_verification, password_recovery, \
    UserListView, user_toggle_activity, UserDitailView, UserDeleteView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:pk>/', UserDitailView.as_view(), name='user'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('verification/', email_verification, name='verification'),
    path('recovery/', password_recovery, name='recovery'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('user/activity/<int:pk>/', user_toggle_activity, name='user_activity'),
]
