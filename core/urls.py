from django.urls import path
from .views import (
    ShanyrakCreateView,
    ShanyrakDetailView,
    ShanyrakUpdateView,
    ShanyrakDeleteView,
    CommentCreateView,
    CommentListView,
    CommentUpdateView,
    CommentDeleteView,
    ShanyrakListView 
)

urlpatterns = [
    path('', ShanyrakListView.as_view(), name='shanyrak-list'), 
    path('create/', ShanyrakCreateView.as_view(), name='create_shanyrak'),
    path('<int:id>/', ShanyrakDetailView.as_view(), name='detail_shanyrak'),
    path('<int:id>/update/', ShanyrakUpdateView.as_view(), name='update_shanyrak'),
    path('<int:id>/delete/', ShanyrakDeleteView.as_view(), name='delete_shanyrak'),
    path('<int:shanyrak_id>/comments', CommentCreateView.as_view(), name='add_comment'),
    path('<int:shanyrak_id>/comments', CommentListView.as_view(), name='list_comments'),
    path('<int:shanyrak_id>/comments/<int:comment_id>/update/', CommentUpdateView.as_view(), name='update_comment'),
    path('<int:shanyrak_id>/comments/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
]