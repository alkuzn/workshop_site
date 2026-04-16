from rest_framework.permissions import BasePermission
from rest_framework.request import Request,HttpRequest
from rest_framework.permissions import SAFE_METHODS
from apps.orders.models.order import Order
from apps.common.roles import Roles

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
            repairman=request.user
        ).exists() or request.method in SAFE_METHODS:
            return True
        return False

class GroupBasedPermissions(BasePermission):
    """Разрешение доступно только членам указанной группы."""
    group_required = []

    def has_permission(self, request, view):
        groups = set(request.user.groups.values_list('name', flat=True))
        required_groups = set(self.group_required)
        return bool(required_groups & groups)

class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.creator == request.user
    
