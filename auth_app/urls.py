from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserDetailView, UserUpdateView

urlpatterns = [
    path('users/', UserRegistrationView.as_view(), name='register'),
    path('users/login', UserLoginView.as_view(), name='login'),
    path('users/me', UserDetailView.as_view(), name='profile'),
    path('users/me', UserUpdateView.as_view(), name='update_profile'),
]