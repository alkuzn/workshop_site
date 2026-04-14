from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import DjangoModelPermissions, AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer

from apps.orders.models.order import Order
from apps.orders.serializers import order_serializers

from apps.common.permissions import IsDispatcherOrReadOnly,GroupBasedPermissions
from apps.common.roles import Roles

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    permission_classes = [DjangoModelPermissions, IsDispatcherOrReadOnly]
    #throttle_classes
    #authentication_classes

    serializers = {
        "list":{
            Roles.dispatcher.value: order_serializers.OrderSerializerViewDispatcher,
            Roles.repairman.value: order_serializers.OrderSerializerViewRepairman,
            Roles.client.value: order_serializers.OrderSerializerViewClient,
        },
        "create":{
            Roles.dispatcher.value: order_serializers.OrderSerializerCreate,
        },
        "partial_update":{
            Roles.dispatcher.value: order_serializers.OrderSerializerUpdate
        },
        "update":{
            Roles.dispatcher.value: order_serializers.OrderSerializerUpdate
        },
        "retrieve":{
            Roles.dispatcher.value: order_serializers.OrderSerializerViewDetails,
        }
    }

    def get_permissions(self):
        return super().get_permissions()
        new = type(#Чтобы получать список заказов, юзер должен быть в группе
            'GeneratedGroupBasedPermissions',
            (GroupBasedPermissions,), 
            {'group_required': [self.kwargs['role']]})#Пока так, но роль должна передаваться в токене\теле\заголовке. И\или меняться отдельной ручкой?
        self.permission_classes.append(new)
        return super().get_permissions()

    def get_serializer_class(self):
        role = self.kwargs.get('role', Roles.dispatcher.value)####ЭТО ДЛЯ ТЕСТА!УБРАТЬ!
        serializer_class = self.serializers[self.action][role]
        return serializer_class

    def get_queryset(self):
        return super().get_queryset()#Пока не знаю как фильтровать для мастеров и прочих
        user = self.request.user
        role = self.kwargs['role']
        filter = {}
        if Roles.repairman.value == role:
            #Мастер может получить инфо о заказе, только если у него есть таска к этому заказу
            filter["repairman"] = user
        elif Roles.client.value  == role:
            self.queryset.filter(client = user)
        if filter:
            return models.Order.objects.filter(**filter)
        else:
            return super().get_queryset()
    
    #def perform_create(self, serializer: Serializer):
    #   этот метод мне тут вообще не нужен?
    #    serializer.save()
    
    def perform_update(self, serializer):
        #Если заявка оплачена, то изменять её нельзя
        return super().perform_update(serializer)
