from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from store.models import Product
from category.models import Category
from carts.models import Cart,CartItem
from carts.views import _cart_id
from django.http import HttpResponse
############ Nur fur fuction views ######################
from django.core.paginator import Paginator
from store.models import Publication,Article
# Create your views here.
class StoreView(ListView):
    model=Product
    paginate_by = 6
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
    def get_context_data(self):
        context=super().get_context_data()
        try:
            cart=Cart.objects.get(cart_id=_cart_id(self.request))
        except Cart.DoesNotExist:
            _cart_id(request)
            cart=None
        added_to_cart=CartItem.objects.all().filter(cart=cart)
        in_cart=[]
        for item in added_to_cart:
            in_cart.append(item.product_id)
        context['in_cart']=in_cart

        #return HttpResponse(added_to_cart)
        return context


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product=Product.objects.order_by('-created_date').filter(description__contains=keyword)
            paginator = Paginator(product, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context={'product_list':product,'page_obj':page_obj,'keyword':keyword}
        else:
            product=Product.objects.order_by('-created_date')
            paginator = Paginator(product, 4)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            keyword='?keyword='
            context={'product_list':product,'page_obj':page_obj,'keyword':keyword}
    return render(request,'shopapp/search-result.html',context)




class ProductView(DetailView):
    model=Product
    template_name='shopapp/product-detail.html'




def product_detail(request,category_slug,slug):
    template_name='shopapp/product-detail.html'
    product=Product.objects.get(category__slug=category_slug,slug=slug)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        _cart_id(request)
        cart=None
    in_cart=CartItem.objects.filter(cart=cart,product=product).exists()
    context={'product':product,'in_cart':in_cart}
    return render(request,template_name, context)



def test(request):
    # Publication objects have access to their related Article objects:
    entesharat=Publication.objects.get(name='Ghalam Tschi')
    kotob=entesharat.article_set.all()
    return HttpResponse(Index(F('height') * F('weight'), Round('weight'), name='calc_idx'))
    ##########################################################
#    ketab=Article.objects.get(titr='sex in 10 minutes')
#    entesharat=ketab.publications.all()
#    for en in entesharat:
#        return HttpResponse(en.name)

###################################################################
#    entesharat=Publication.objects.get(name='Ghalam Tschi')
#    ketab=Article.objects.filter(publications=entesharat)
#    return HttpResponse(ketab)
