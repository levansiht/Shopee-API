from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from backend_api.serializers import UserUpdateSerializer, AvatarUploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)
    
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UploadAvatarView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = AvatarUploadSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            image = serializer.validated_data['image']
            path = default_storage.save(f'avatars/{user.id}/{image.name}', ContentFile(image.read()))
            user.userprofile.avatar = path
            user.userprofile.save()
            return Response({"message": "Avatar uploaded successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)