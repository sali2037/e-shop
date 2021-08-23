from django.urls import path
from carts import views
app_name='carts'
urlpatterns=[
        path('', views.carts,name='show_carts' ),
        path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
        path('add_cart/<int:product_id>/<slug:minus>',views.add_cart,name='add_cart_minius'),
        path('remove_cart_item/<int:product_id>',views.remove_cart_item,name='remove_item'),
        path('testcookie/', views.cookie_session),
        path('deletecookie/', views.cookie_delete),
        path('cartcookie/', views.cart_cookie),
        path('access_session/', views.access_session),
        

]
