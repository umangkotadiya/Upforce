from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer ,LikeSerializer
from django.shortcuts import get_object_or_404
from .custom_permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PostListCreateView(generics.ListCreateAPIView):
    print("PostListCreateView---------")
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsOwnerOrReadOnly]

        
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

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer