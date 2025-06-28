from django.contrib import admin
import admin_thumbnails
from store.models import (
    Category, Brand, Product, ProductImages, Variations, BannerOverlay, DealsOutlet
)

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}   
    list_display = ['id', 'title', 'slug', 'image_tag', 'featured', 'popular', 'status', 'created_date', 'updated_date']
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}   
    list_display = ['id', 'title', 'slug', 'image_tag', 'featured', 'popular', 'status', 'created_date', 'updated_date']
admin.site.register(Brand, BrandAdmin)

@admin_thumbnails.thumbnail('gallery')
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    prepopulated_fields = {'slug': ('title',)}   
    list_display = ['id', 'category', 'brand', 'title', 'slug', 'price', 'old_price', 'in_stock_total', 'discount', 'discount_price', 'description', 'additiona_des', 'shipping_return', 'featured', 'trending', 'top_deals', 'popular', 'new_arrivals', 'recommendation', 'in_stock', 'status', 'created_date', 'updated_date']
admin.site.register(Product, ProductAdmin)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_tag', 'created_date', 'updated_date']
admin.site.register(ProductImages, ImagesAdmin)

class VariationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'variation', 'title', 'image_tag', 'price', 'created_date', 'updated_date']
admin.site.register(Variations, VariationsAdmin)

admin.site.register([BannerOverlay, DealsOutlet])