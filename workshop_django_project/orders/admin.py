from django.contrib import admin
from orders.models import Order, Machine, MachineType, Mark, OrderStatus, Street,Settlement, Job, ServiceCall,ServiceCallType
from orders import models
# Register your models here.

admin.site.register([Order, Machine, MachineType, Mark, OrderStatus, Street, Settlement, Job, ServiceCallType, ServiceCall])