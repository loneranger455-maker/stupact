import imp
from django.contrib import admin
from dataforstupact.models import mymodel,stumartmodel,order_list,notifications,verifyrequest
# Register your models here.
class serviceadmin(admin.ModelAdmin):
    list_display=("username","password")
class stumart_class(admin.ModelAdmin):
    list_display=("id","title","image")
class order_class(admin.ModelAdmin):
    list_display=("product","buyer","seller","phonenumber")
class notify_class(admin.ModelAdmin):
    list_display=("username","notify","status")
class verify_class(admin.ModelAdmin):
    list_display=("username","filevalue")
admin.site.register(mymodel,serviceadmin)
admin.site.register(stumartmodel,stumart_class)
admin.site.register(order_list,order_class)
admin.site.register(notifications,notify_class)
admin.site.register(verifyrequest,verify_class)