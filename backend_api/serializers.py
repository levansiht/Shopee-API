
from rest_framework import serializers
from .models import Category, Product, Cart, Product, CartItem, User, UserProfile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'images', 'price', 'rating', 'price_before_discount', 'quantity',
            'sold', 'view', 'name', 'description', 'category', 'image', 'created_at', 'updated_at'
        ]
    
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['product', 'product_id', 'quantity']

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value

    def validate_quantity(self, value):
        if value is None:
            raise serializers.ValidationError("Quantity cannot be null.")
        return value


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    buy_count = serializers.IntegerField(min_value=1)
    

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    date_of_birth = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'address', 'date_of_birth', 'avatar', 'email']

    def get_email(self, obj):
        return obj.user.email


class UserUpdateSerializer(serializers.ModelSerializer):
    data = UserProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = ['data', 'email']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        email = validated_data.get('email', instance.email)

        instance.email = email
        instance.save()

        profile = instance.userprofile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance
    
class AvatarUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        if value.size > 1024 * 1024:  # 1MB
            raise serializers.ValidationError("Image file too large ( > 1MB )")
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("File is not an image")
        return value