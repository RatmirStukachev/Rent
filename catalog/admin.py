from django.contrib import admin
from .models import Category, Product, ProductCharacteristic, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_per_day', 'status']
    list_filter = ['category', 'status']
    list_editable = ['price_per_day', 'status']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductCharacteristicInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer_name', 'customer_phone', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'product__name']
    list_editable = ['status']
