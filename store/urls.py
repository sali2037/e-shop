from django.urls import path
from store import views

app_name='store'
urlpatterns = [

    #path('<slug:slug>/',views.ProductView.as_view(), name='product_detail'),
    path('',views.StoreView.as_view(), name='store'),
    path('category/<slug:category_slug>/',views.StoreView.as_view(), name='product_by_cate'),
    #path('<slug:category_slug>/<slug:slug>/',views.ProductView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/product/<slug:slug>/',views.product_detail, name='product_detail'),
    path('submit-reveiw/<int:product_id>',views.submit_reveiw, name='submit_review'),
    path('search/', views.search, name='search'),
    path('test/', views.test, name='test'),


]
