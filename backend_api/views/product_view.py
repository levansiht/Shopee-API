from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from backend_api.models import Product
from backend_api.serializers import ProductSerializer
from backend_api.views.commom import CustomPageNumberPagination


class ProductListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        query_params = request.query_params
        products = Product.objects.all()

        filters = {
            'category_id': query_params.get('category'),
            'rating__gte': query_params.get('rating_filter'),
            'price__lte': query_params.get('price_max') if query_params.get('price_max') else None,
            'price__gte': query_params.get('price_min') if query_params.get('price_min') else None,
            'name__icontains': query_params.get('name')
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        products = products.filter(**filters)

        exclude = query_params.get('exclude')
        if exclude:
            products = products.exclude(id=exclude)

        search = query_params.get('search')
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )

        sort_by_mapping = {
            'createdAt': 'created_at',
            'view': 'view',
            'sold': 'sold',
            'price': 'price'
        }
        sort_by = sort_by_mapping.get(query_params.get('sort_by', 'created_at'), 'created_at')
        order = query_params.get('order', 'desc')
        if order == 'desc':
            sort_by = f'-{sort_by}'
        products = products.order_by(sort_by)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({
            "message": "Lấy sản phẩm thành công",
            "data": serializer.data
        })