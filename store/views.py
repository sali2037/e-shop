from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from store.models import Product
from category.models import Category

# Create your views here.
class StoreView(ListView):
    model=Product
    template_name='shopapp/store.html'
    queryset=Product.objects.all().filter(is_available = True)
    def get_queryset(self):
        queryset=super().get_queryset()
        if self.kwargs:
            slug=self.kwargs['category_slug']
            categories= get_object_or_404(Category,slug=slug)
            return queryset.filter(is_available = True,category=categories)
        else:
            return queryset.filter(is_available = True)
class ProductView(DetailView):
    model=Product
    template_name='shopapp/product-detail.html'

def product_detail(request,category_slug,slug):
    template_name='shopapp/product-detail.html'
    product=Product.objects.get(category__slug=category_slug,slug=slug)
    context={'product':product} 
    return render(request,template_name, context)
