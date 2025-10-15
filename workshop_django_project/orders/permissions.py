from rest_framework.permissions import BasePermission
from rest_framework.request import Request,HttpRequest
from rest_framework.permissions import SAFE_METHODS
from orders.models import Order
from orders.roles import Roles

class IsRepairman(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="repairman").exists():
            return True
        return False 
    
class IsSupplymanager(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="supplymanager").exists():
            return True
        return False 

class IsDispatcherOrReadOnly(BasePermission):
    def has_permission(self, request: HttpRequest, view):
        if request.user.groups.filter(name=Roles.dispatcher.value).exists() or request.method in SAFE_METHODS:
            return True
        return False 
    
class IsNotSupplymanager(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="supplymanager").exists():
            return False
        return True 

class IsRepairmanOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if Order.objects.filter(
            id=view.kwargs['order_id'],
            repairman_id=request.user.id
        ).exists() or request.method in SAFE_METHODS:
            return True
        return False