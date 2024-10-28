from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from backend_api.models import Cart, CartItem, Product
from backend_api.serializers import AddToCartSerializer

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            buy_count = serializer.validated_data['buy_count']
            user = request.user

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"message": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

            cart, created = Cart.objects.get_or_create(user=user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, status=CartItem.Status.IN_CART.value)
            if created:
                cart_item.quantity = buy_count
                cart_item.status = CartItem.Status.IN_CART
            else:
                cart_item.quantity += buy_count
            cart_item.save()

            response_data = {
                "message": "Thêm sản phẩm vào giỏ hàng thành công",
                "data": {
                    "buy_count": cart_item.quantity,
                    "price": product.price,
                    "price_before_discount": product.price_before_discount,
                    "status": cart_item.status,  
                    "id": cart_item.id,
                    "user": user.id,
                    "product": {
                        "images": [image for image in product.images],
                        "price": product.price,
                        "rating": product.rating,
                        "price_before_discount": product.price_before_discount,
                        "quantity": product.quantity,
                        "sold": product.sold,
                        "view": product.view,
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "category": {
                            "id": product.category.id,
                            "name": product.category.name,
                        },
                        "image": product.image,
                    },
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart, status=CartItem.Status.IN_CART.value)

        response_data = {
            "message": "Lấy đơn mua thành công",
            "data": []
        }

        for cart_item in cart_items:
            product = cart_item.product
            item_data = {
                "id": cart_item.id,
                "buy_count": cart_item.quantity,
                "price": product.price,
                "price_before_discount": product.price_before_discount,
                "status": cart_item.status,
                "user": user.id,
                "product": {
                    "id": product.id,
                    "images": [image for image in product.images],  
                    "price": product.price,
                    "rating": product.rating,
                    "price_before_discount": product.price_before_discount,
                    "quantity": product.quantity,
                    "sold": product.sold,
                    "view": product.view,
                    "name": product.name,
                    "description": product.description,
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name,
                    },
                    "image": product.image,
                    "createdAt": product.created_at.isoformat(),
                    "updatedAt": product.updated_at.isoformat(),
                },
                "createdAt": cart_item.created_at.isoformat(),
                "updatedAt": cart_item.updated_at.isoformat(),
            }
            response_data["data"].append(item_data)

        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        response_data = {
            "message": "Cập nhật đơn thành công",
            "data": []
        }

        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            buy_count = serializer.validated_data['buy_count']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"message": f"Product with id {product_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity = buy_count
            cart_item.status = CartItem.Status.IN_CART
            cart_item.save()

            item_data = {
                "id": cart_item.id,
                "buy_count": cart_item.quantity,
                "price": product.price,
                "price_before_discount": product.price_before_discount,
                "status": cart_item.status,
                "user": user.id,
                "product": {
                    "id": product.id,
                    "images": [image for image in product.images],
                    "price": product.price,
                    "rating": product.rating,
                    "price_before_discount": product.price_before_discount,
                    "quantity": product.quantity,
                    "sold": product.sold,
                    "view": product.view,
                    "name": product.name,
                    "description": product.description,
                    "category": {
                        "id": product.category.id,
                        "name": product.category.name,
                    },
                    "image": product.image,
                    "createdAt": product.created_at.isoformat(),
                    "updatedAt": product.updated_at.isoformat(),
                },
                "createdAt": cart_item.created_at.isoformat(),
                "updatedAt": cart_item.updated_at.isoformat(),
            }
            response_data["data"].append(item_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item_ids = request.data
        cart_items = CartItem.objects.filter(cart=cart, id__in=cart_item_ids, status=CartItem.Status.IN_CART.value)
        
        if not cart_items.exists():
            return Response({"message": "No cart items found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items.delete()
        return Response({"message": "Xóa giỏ hàng thành công"}, status=status.HTTP_200_OK)

class BuyProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        response_data = {
            "message": "Mua sản phẩm thành công",
            "data": []
        }

        for item in request.data:
            serializer = AddToCartSerializer(data=item)
            if serializer.is_valid():
                product_id = serializer.validated_data['product_id']
                buy_count = serializer.validated_data['buy_count']

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return Response({"message": f"Product with id {product_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

                cart, created = Cart.objects.get_or_create(user=user)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    cart_item.quantity = buy_count
                else:
                    cart_item.quantity += buy_count
                cart_item.status = CartItem.Status.WAIT_FOR_CONFIRMATION
                cart_item.save()

                response_data["data"].append({
                    "buy_count": cart_item.quantity,
                    "price": product.price,
                    "price_before_discount": product.price_before_discount,
                    "status": cart_item.status,
                    "id": cart_item.id,
                    "user": user.id,
                    "product": {
                        "images": [image for image in product.images],
                        "price": product.price,
                        "rating": product.rating,
                        "price_before_discount": product.price_before_discount,
                        "quantity": product.quantity,
                        "sold": product.sold,
                        "view": product.view,
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "category": {
                            "id": product.category.id,
                            "name": product.category.name,
                        },
                        "image": product.image,
                    },
                })
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_201_CREATED)