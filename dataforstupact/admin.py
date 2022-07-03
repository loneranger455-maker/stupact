import imp
from django.contrib import admin
from dataforstupact.models import mymodel
# Register your models here.
class serviceadmin(admin.ModelAdmin):
    list_display=("username","password")
admin.site.register(mymodel,serviceadmin)