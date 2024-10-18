from django.urls import path
from .views import (
    PostListCreateView, PostDetailView, LikePostView ,CreateUserView ,LoginView ,UserDetailView
)

urlpatterns = [
    path('accounts/', CreateUserView.as_view(), name='create_account'),
    path('accounts/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('blog/', PostListCreateView.as_view(), name='post-list-create'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('like/<int:blog_id>/', LikePostView.as_view(), name='like-post'),
]
