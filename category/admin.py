from django.contrib import admin
from category.models import Category

#automatische Admin SlugField
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields    = {'slug' : ('category_name',)}
    list_display           = ('category_name','slug')
    list_display_links     = ('category_name','slug')



# Register your models here.
admin.site.register(Category,CategoryAdmin)
