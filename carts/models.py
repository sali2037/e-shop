from django.db import models
from store.models import Product,Variation
from accounts.models import Account
# Create your models here.
class Cart(models.Model):
    cart_id      = models.CharField(max_length=200,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user           = models.ForeignKey(Account,null=True,on_delete=models.CASCADE,default=None)
    product        = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='products')
    cart           = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    is_active      = models.BooleanField(default=True)
    variations     = models.ManyToManyField(Variation,blank=True)


    def get_price(self):
        return round(self.product.price*self.quantity,2) 

    def __str__(self):
        return self.product.product_name
