from django.urls import path
from shopapp import views
app_name='shopapp'
urlpatterns = [
    #path('',views.home,name='home'),
    path('', views.HomeView.as_view(), name='home'),
    #path('store',views.StoreView.as_view(), name='store'),
]
