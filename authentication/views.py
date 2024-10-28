# authentication/views.py
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.utils.text import slugify

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({
                "message": "Đăng ký thất bại",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            "message": "Đăng ký thành công",
            "data": {
                "access_token": f"Bearer {str(refresh.access_token)}",
                "refresh_token": str(refresh),
                "expires": "7d",
                "user": UserSerializer(user).data
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        username = slugify(email.split('@')[0])
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = {
                "message": "Đăng nhập thành công",
                "data": {
                    "access_token": f"Bearer {str(refresh.access_token)}",
                    "refresh_token": str(refresh),
                    "expires": "7d",
                    "user": UserSerializer(user).data
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)