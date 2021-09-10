from django.db import models
from accounts.models import Account
from store.models import Variation,Product

# Create your models here.
class Payment(models.Model):
    user            = models.ForeignKey(Account,on_delete = models.CASCADE)
    payment_id      = models.CharField(max_length=200)
    peyment_method  = models.CharField(max_length=200)
    amount_paid     = models.CharField(max_length=200)
    status          = models.CharField(max_length=200)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
class Order(models.Model):
        STATUS     = (
            ('New','New'),
            ('Accepted','Accepted'),
            ('Completed','Completed'),
            ('Cancelled','Cancelled')
        )
        user         = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
        payment      = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
        order_numer  = models.CharField(max_length=200, unique=True)
        first_name   = models.CharField(max_length=200)
        last_name    = models.CharField(max_length=200)
        phone        = models.CharField(max_length=200)
        email        = models.EmailField()
        country      = models.CharField(max_length=200)
        state        = models.CharField(max_length=200)
        street       = models.CharField(max_length=250)
        hause_number = models.IntegerField()
        postalconde  = models.CharField(max_length=12)
        tax          = models.FloatField(default=1.2)
        ip           = models.CharField(blank=True,max_length=200)
        status       = models.CharField(max_length=20,choices=STATUS,default='New')
        is_ordered   = models.BooleanField(default=False)
        created_at   = models.DateTimeField(auto_now_add=True)
        updated_at   = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.user.first_name

class OrderProduct(models.Model):
    order            = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment          = models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True)
    user             = models.ForeignKey(Account,on_delete=models.CASCADE)

    product          = models.ForeignKey(Product,on_delete=models.CASCADE)
    color            = models.CharField(max_length=50)
    size             = models.CharField(max_length=50)
    quantity         = models.IntegerField()
    ordered          = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.product_name
