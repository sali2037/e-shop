from carts.models import Cart,CartItem
from carts.views import _cart_id

def artikel_number(request):
    num=0
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.all().filter(user=request.user)
        else:
            cart_id=_cart_id(request)
            cart=Cart.objects.get(cart_id=cart_id)
            cart_item=CartItem.objects.all().filter(cart=cart.id)
        for item in cart_item:
            num+=item.quantity
    except Cart.DoesNotExist:
        num=0

    return dict(num=num)
