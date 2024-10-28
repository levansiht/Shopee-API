
from django.contrib import admin
from django.urls import path, include
from backend_api.views import product_view, cart_view, category_view, user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_view.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', product_view.ProductDetailView.as_view(), name='product-detail'),
    path('categories/', category_view.CategoryListView.as_view(), name='category-list'),
    path('purchases/add-to-cart/', cart_view.AddToCartView.as_view(), name='add-to-cart'),  
    path('purchases/', cart_view.AddToCartView.as_view(), name='get-cart'), 
    path('purchases/buy-products/', cart_view.BuyProductView.as_view(), name='buy-cart'), 
    path('purchases/update-purchase/', cart_view.AddToCartView.as_view(), name='update-purchase'), 
]
urlpatterns += [
    path('auth/', include('authentication.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('me', user_view.UserProfileView.as_view(), name='user-profile'),
    path('user', user_view.UserUpdateView.as_view(), name='user-update'),
    path('user/upload-avatar', user_view.UploadAvatarView.as_view(), name='upload-avatar'),
]

    