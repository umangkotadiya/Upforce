from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    # RegisterView, LoginView, UserDetailView,
    PostListCreateView, PostDetailView, LikePostView ,CreateUserView ,MyTokenObtainPairView
)

urlpatterns = [
    path('accounts/', CreateUserView.as_view(), name='create_account'),
    path('accounts/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
    # path('accounts/', RegisterView.as_view(), name='register'),
    # path('accounts/login/', LoginView.as_view(), name='login'),
    # path('accounts/<int:pk>/', UserDetailView.as_view(), name='user-detail-update-delete'),
    # path('accounts/me/', UserDetailView.as_view(), name='user-detail'),

    path('blog/', PostListCreateView.as_view(), name='post-list-create'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('like/<int:blog_id>/', LikePostView.as_view(), name='like-post'),
]
