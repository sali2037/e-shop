from carts.models import Cart,CartItem
from carts.views import _cart_id

def artikel_number(request):
    num=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=None
    cart_item=CartItem.objects.all().filter(cart=cart)
    for item in cart_item:
        num+=item.quantity
    return dict(num=num)
