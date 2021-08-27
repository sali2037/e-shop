from django.urls import path
from accounts import views
app_name='accounts'
urlpatterns=[
    path('register/', views.RegisterView.as_view(),              name='register'),
    path('login/',    views.Login.as_view(),                     name='login'),
    path('activate/<uidb64>/<token>/',views.activate,            name='activate'),
    path('dashboard/',views.DashboardView.as_view(),             name='dashboard'),
    path('resetpass/',views.Resetpass.as_view(),                 name='resetpass'),
    path('resetform/<uidb64>/<token>/',views.change_password,    name='reset_form')
    ]
