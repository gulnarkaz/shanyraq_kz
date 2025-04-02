from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserDetailView, UserUpdateView, AddToFavoritesView, FavoriteShanyrakListView, RemoveFromFavoritesView

urlpatterns = [
    path('users/', UserRegistrationView.as_view(), name='register'),
    path('users/login', UserLoginView.as_view(), name='login'),
    path('users/me', UserDetailView.as_view(), name='profile'),
    path('users/me', UserUpdateView.as_view(), name='update_profile'),
    path('users/favorites/shanyraks/<int:id>', AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('users/favorites/shanyraks', FavoriteShanyrakListView.as_view(), name='favorite_shanyraks_list'),
     path('users/favorites/shanyraks/<int:id>', RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
]