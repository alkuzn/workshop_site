from django.contrib import admin

from apps.orders.models.order import Order
from apps.orders.models.address import Settlement, Street
from apps.orders.models.machine import Brand, MachineType

admin.site.register([
    Order, 
    MachineType, 
    Brand,
    Street, 
    Settlement, 
])