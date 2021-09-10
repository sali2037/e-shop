from django.shortcuts import render
from django.views.generic import FormView
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from order.forms import OrderForm
from carts.models import CartItem
from store.models import Product
from order.models import Order,Payment,OrderProduct
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import json
from django.http import JsonResponse
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
# Create your views here.

class Checkout( LoginRequiredMixin ,FormView):
    template_name ='shopapp/place-order.html'
    form_class    = OrderForm
    success_url   = '/order/payment/'

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        cart_item     = CartItem.objects.filter(user_id=self.request.user)
        total_price=0
        for item in cart_item:
            total_price += item.get_price()
        tax_price     = (total_price*10)/100
        totalTax      = tax_price + total_price
        context['total_price']  = total_price
        context['tax_price']    = tax_price
        context['cart_items']   = cart_item
        context['totalTax']  = totalTax
        return context
    def form_valid(self,form):
        from datetime import datetime
        order            = form.save()
        order.user       = self.request.user
        context          = self.get_context_data()
        order.tax        = round(context['tax_price'],2)
        now              = datetime.now() # current date and time
        heute            = now.strftime("%y%m%d%S%H")
        order_numer      = str(heute)+str(self.request.user.pk)
        order.order_numer= order_numer
        order.ip         = self.request.META.get('REMOTE_ADDR')
        order.save()
        ##################################
        try:
            order=Order.objects.get(user=self.request.user,is_ordered=False,order_numer= order_numer)
            template_name = 'shopapp/payment.html'
            return render(self.request,template_name,context={'cart_items':context['cart_items'],'total_price':context['total_price'],'totalTax':context['totalTax'],'tax_price':context['tax_price'],'order':order})
        except Order.MultipleObjectsReturned:
            order=Order.objects.filter(user=self.request.user,is_ordered=False,order_numer= order_numer)
            order.delete()
            return HttpResponseRedirect(reverse('order:checkout'))

#        return super().form_valid(form)


def payments(request):
    body= json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_numer=body['orderID'])
    payment=Payment()
    payment.user       = request.user
    #amount=body['transaction']['amount']['value']
    payment.amount_paid = body['amount']
    payment.payment_id = body['transactionID']
    payment.peyment_method=body['payment_method']
    payment.status=body['status']
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    ########### move item from cartitem to order product table
    cart_item=CartItem.objects.filter(user=request.user)
    for item in cart_item:
        order_product = OrderProduct()
        order_product.order     = order
        order_product.payment   = payment
        order_product.user      = request.user
        order_product.product   = item.product
        order_product.quantity  = item.quantity
        order_product.ordered   = True
        for variation in item.variations.all():
            if variation.variation_category=="color":
                order_product.color = variation.variation_value
            if variation.variation_category=="size":
                order_product.size = variation.variation_value
        order_product.save()
    #############Reduce die Stock ##########################

    for item in cart_item:
        product=Product.objects.get(id=item.product_id)
        product.stock  =product.stock- item.quantity
        if product.stock <1 :
            product.is_available = False
        product.save()
    ######################clear carts #######################
    cart_item.delete()
    #################send Email to Customer##################
    orderproduct=OrderProduct.objects.filter(user=request.user,order=order,payment=payment)
    total_price=0
    for item in orderproduct:
        total_price += item.product.price*item.quantity
    tax_price=round((2*total_price)/100,2)
    totalTax=total_price+tax_price

    mail_subject  = 'Einkauf Datails'
    mail_to       = request.user.email
    email_body    = render_to_string('shopapp/bestetigungEmail.html',{
    'order':order,
    'orderproducts':orderproduct,
    'total_price':round(total_price,2),
    'tax_price':round(tax_price,2),
    'totalTax':round(totalTax,2)

    })
    send_email    = EmailMessage(mail_subject,email_body,to=[mail_to])
    send_email.content_subtype = "html"
    send_email.send()


    # Send order und number of transaction to data Jsone ############
    data={
    'orderID'   : order.order_numer,
    'payment_id': payment.payment_id,
    }
    return JsonResponse(data)


def order_complate(request):
    try:
        order_id=request.GET.get('orderID')
        payment=Payment.objects.get(payment_id=request.GET.get('payment_id'))
        order=Order.objects.get(user=request.user, order_numer=order_id,is_ordered=True,payment=payment)
        orderproduct=OrderProduct.objects.filter(user=request.user,order=order,payment=payment)
        total_price=0
        for item in orderproduct:
            total_price += item.product.price*item.quantity
        tax_price=round((2*total_price)/100,2)
        totalTax=total_price+tax_price
        template_name='shopapp/order_complate.html'
        return render(request, template_name,context={'order':order,'payment':payment,'orderproducts':orderproduct,'total_price':total_price,'tax_price':tax_price,'totalTax':totalTax})
    except (Payment.DoesNotExist,Order.DoesNotExist):
        messages.success(request, 'Etwas schif gelaufen')
        return HttpResponseRedirect(reverse('accounts:dashboard'))
