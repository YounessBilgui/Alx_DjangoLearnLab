
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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

class FollowUserView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, user_id):
		target = get_object_or_404(User, id=user_id)
		if target == request.user:
			return Response({'detail': 'Cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
		request.user.following.add(target)
		return Response({'detail': f'Now following {target.username}'}, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, user_id):
		target = get_object_or_404(User, id=user_id)
		if target == request.user:
			return Response({'detail': 'Cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
		request.user.following.remove(target)
		return Response({'detail': f'Stopped following {target.username}'}, status=status.HTTP_200_OK)
