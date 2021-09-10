from django.urls import path
from order import views
app_name='order'
urlpatterns=[
        path('checkout/',views.Checkout.as_view(),         name='checkout'),
        path('payment/',views.payments,                    name='payment'),
        path('order-complate/',views.order_complate,name='order_complate')
    ]
