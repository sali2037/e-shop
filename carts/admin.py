from django.contrib import admin
from carts.models import Cart,CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity','is_active')
    list_editable= ('is_active',)

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
