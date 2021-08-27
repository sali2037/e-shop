from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView,CreateView
from store.models import Product,Variation
from carts.models import Cart,CartItem
# Create your views here.

def carts(request):
    try:
        cart_id=_cart_id(request)
        cart=Cart.objects.get(cart_id=cart_id)
        cart_items=CartItem.objects.all().filter(cart=cart.id)
        total_price=0
        for item in cart_items:
            total_price += item.product.price*item.quantity
        tax_price=round((2*total_price)/100,2)
        totalTax=total_price+tax_price

        context={'cart':cart,'cart_items':cart_items,'total_price':round(total_price,2),'totalTax':totalTax,'tax_price':tax_price}

        return render(request, 'shopapp/cart.html',context)
    except CartItem.DoesNotExist:
        pass



def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id,minus=None):
    product=Product.objects.get(pk=product_id)
    if request.method == 'GET':
        variation_list=[]
        for item in request.GET:
            try:
                variation_obj=Variation.objects.get(product_id=product_id,pk=request.GET[item])
                variation_list.append(variation_obj)
            except Variation.DoesNotExist:
                pass
    try:
        cart_id=_cart_id(request)
        if  not cart_id:
            cart_id=_cart_id(request)
        cart=Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart= Cart.objects.create(cart_id=cart_id)
    cart.save()
############################
    cart_exist = CartItem.objects.filter(product_id=product.id,cart_id=cart).exists()
    if cart_exist:
        cart_item=CartItem.objects.filter(product=product,cart=cart)
        if len(variation_list) > 0:
            existing_variation=[]
            id=[]
            for item in cart_item:
                ex_variation = item.variations.all()
                existing_variation.append(list(ex_variation))
                id.append(item.id)
            if variation_list in existing_variation:
                index= existing_variation.index(variation_list)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                if minus:
                    if item.quantity >1:
                        item.quantity-=1
                    else:
                        item.delete()
                else:
                    item.quantity+=1
            else:
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                for vari in variation_list:
                    item.variations.add(vari)
            item.save()
            return HttpResponseRedirect(reverse_lazy('carts:show_carts'))
    else:
        cart_item=CartItem.objects.create(
                                        product=product,
                                        cart=cart,
                                        quantity=1,
                                        is_active=True)
        if len(variation_list) > 0:
            for vari in variation_list:
                cart_item.variations.add(vari)
        cart_item.save()
        if cart_item:
            return HttpResponseRedirect(reverse('carts:show_carts'))
        else:
            return HttpResponseRedirect(reverse('store:product_by_cate'))


def remove_cart_item(request,product_id):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        product=Product.objects.get(id=product_id)
        cart_item=CartItem.objects.filter(cart=cart,product=product).delete()
        return HttpResponseRedirect(reverse('carts:show_carts'))
    except CartItem.DoesNotExist:
        return HttpResponseRedirect(reverse('carts:show_carts'))




def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse("<h1>dataflair</h1>")
def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("dataflair<br> cookie createed")
    else:
        response = HttpResponse("Dataflair <br> Your browser doesnot accept cookies")
    return response

def access_session(request):
    response = "<h1>Welcome to Sessions of dataflair</h1><br>"
    if request.session.get('name'):
        response += "Name : {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "Password : {0} <br>".format(request.session.get('password'))
        return HttpResponse(response)
    else:
        return redirect('cart_cookie/')



def cart_cookie(request):
    request.session.create()

    request.session['name'] = 'Ali'
    request.session['password'] = 'Eskandary'
    return HttpResponse('ok')
