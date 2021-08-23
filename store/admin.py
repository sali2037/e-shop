from django.contrib import admin
from store.models import Product,Variation
# Admin Anderungen
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name', 'price', 'stock','is_available','category','created_date','modified_date')
    prepopulated_fields={'slug': ('product_name', )}
class VariationAdmin(admin.ModelAdmin):
    list_display = ( 'product', 'variation_category', 'variation_value','is_active','created_date')
    list_editable= ('is_active',)
    list_filter  = ('product', 'variation_category', 'variation_value')

# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
