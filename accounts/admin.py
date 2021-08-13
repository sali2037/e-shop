from django.contrib import admin
from .models import Account

#um unsere password nur readalbe zu machen
from django.contrib.auth.admin import UserAdmin
class AccountAdmin(UserAdmin):
    list_display=('email','first_name', 'last_name', 'username', 'last_login','date_joined', 'is_active')
    filter_horizontal = ()
    list_filter       = ()
    fieldsets         = ()
    list_display_links= ('email','first_name')
    readonly_fields   = ('last_login','date_joined')
    ordering          = ('-date_joined',)

# Register your models here.
admin.site.register(Account,AccountAdmin)
