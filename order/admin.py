from django.contrib import admin
from order.models import Payment,Order,OrderProduct
# Register your models here.
from django.contrib.auth.admin import UserAdmin
class PaymentAdmin(UserAdmin):
    list_display      = ('user','payment_id','peyment_method','amount_paid','status','created_at')
    filter_horizontal = ()
    list_filter       = ()
    fieldsets         = ()
    ordering          = ('-created_at',)
class OrderAadmin(UserAdmin):
    list_display      = ('user','payment','order_numer','email','status','created_at','updated_at',)
    filter_horizontal = ()
    list_filter       = ()
    fieldsets         = ()
    ordering          = ('-updated_at',)
class OrderProductAdmin(UserAdmin):
    list_display      = ('order','payment','user','product','quantity','created_at',)
    filter_horizontal = ()
    list_filter       = ()
    fieldsets         = ()
    ordering          = ('-updated_at',)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAadmin)
admin.site.register(OrderProduct,OrderProductAdmin)
