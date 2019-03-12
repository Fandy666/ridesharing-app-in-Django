from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from home.models import Owner, Order, Driver

admin.site.register(Owner)
admin.site.register(Order)
admin.site.register(Driver)
