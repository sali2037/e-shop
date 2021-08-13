from django.shortcuts import render
from django.views.generic import ListView
from store.models import Product
# Create your views here.
def home(request):
    return render(request,'shopapp/index.html')
class HomeView(ListView):
    model= Product
    queryset=Product.objects.all().filter(is_available = True)
    template_name='shopapp/index.html'
class StoreView(ListView):
    model=Product
    template_name='shopapp/store.html'
