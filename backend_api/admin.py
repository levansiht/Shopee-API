from django.contrib import admin
from backend_api.models import Product, Category, UserProfile

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_name', 'price', 'quantity', 'sold', 'view')
    list_filter = ('category',)
    def category_name(self, obj):
        return obj.category.name
    category_name.short_description = 'Category'
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

admin.site.register(UserProfile)