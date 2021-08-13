from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name       = models.CharField(max_length=200)
    slug                = models.SlugField(max_length=200, unique=True)
    description         = models.TextField()
    cat_image           = models.ImageField(upload_to='upload_images')

    class Meta:
        verbose_name= 'Group'
        verbose_name_plural='Groupen'
    def get_url(self):
        #return reverse('store:product_by_cate',kwargs={'category_slug':self.slug})
        return reverse('store:product_by_cate',args=[self.slug])
    def __str__(self):
        return self.category_name
