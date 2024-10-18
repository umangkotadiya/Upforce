from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer ,LoginSerializer
from django.shortcuts import get_object_or_404
from .custom_permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

        
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, blog_id):
        try:
            if blog_id:    
                post = get_object_or_404(Post, id=blog_id)
                if Like.objects.filter(post=post, user=request.user).exists():
                    return Response({"message": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    Like.objects.create(post=post, user=request.user)
                return Response({"message": "Liked the post"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Post id not found"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)})
    
    def delete(self, request, blog_id):
        try:
            if blog_id:
                post = get_object_or_404(Post, id=blog_id)
                like = get_object_or_404(Like, post=post, user=request.user)
                if like:
                    like.delete()
                    return Response({"message": "Unliked the post"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"message": "Unliked the post"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Post id not found"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

