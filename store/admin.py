from django.contrib import admin

from store.models import Product, Variation


@admin.register(Product)  # ToDo: Enhance all admins
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'stock', 'category', 'date_modified', 'is_available')


@admin.register(Variation)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'date_created',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')
