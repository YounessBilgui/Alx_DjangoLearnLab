
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserRegistrationSerializer
	permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
	permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveAPIView):
	serializer_class = UserProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return self.request.user
