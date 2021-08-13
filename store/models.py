from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    product_name        = models.CharField(max_length=200,unique=True)
    slug                = models.SlugField(max_length=50,unique=True)
    description         = models.TextField(blank=True)
    price               = models.FloatField()
    image               = models.ImageField(upload_to='product_images')
    farbe               = models.CharField(max_length=100,default='Blau')
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='re_categories')
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('store:product_detail',kwargs={'category_slug':self.category.slug,'slug':self.slug})
