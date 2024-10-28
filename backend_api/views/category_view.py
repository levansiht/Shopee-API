from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from backend_api.models import Category
from backend_api.serializers import CategorySerializer

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all().order_by('-id')
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "message": "Lấy categories thành công",
            "data": serializer.data
        }, status=status.HTTP_200_OK)