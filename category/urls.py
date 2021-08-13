from django.urls import path
from store import views

app_name='category'
urlpatterns = [
    #path('',views.home,name='home'),    
    path('/<slug:category_slug>/',views.StoreView.as_view(), name='store_by_category')
]
