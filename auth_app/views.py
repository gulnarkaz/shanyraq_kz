from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.models import Shanyrak
from auth_app.models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserLoginResponseSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
)
from core.serializers import FavoriteShanyrakSerializer
User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLoginView(views.APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            refresh = RefreshToken.for_user(user)
        except Exception as e:
            return Response({'error': 'Token generation failed', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class AddToFavoritesView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        try:
            shanyrak = get_object_or_404(Shanyrak, id=id)
            request.user.favorites.add(shanyrak)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FavoriteShanyrakListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        favorite_shanyraks = request.user.favorites.all()
        serializer = FavoriteShanyrakSerializer(favorite_shanyraks, many=True)
        return Response({"shanyraks": serializer.data}, status=status.HTTP_200_OK)