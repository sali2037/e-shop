from django.urls import path
from store import views

app_name='store'
urlpatterns = [
    #path('<slug:slug>/',views.ProductView.as_view(), name='product_detail'),
    path('',views.StoreView.as_view(), name='store'),
    path('<slug:category_slug>/',views.StoreView.as_view(), name='product_by_cate'),
    #path('<slug:category_slug>/<slug:slug>/',views.ProductView.as_view(), name='product_detail'),
    path('<slug:category_slug>/<slug:slug>/',views.product_detail, name='product_detail'),

]
