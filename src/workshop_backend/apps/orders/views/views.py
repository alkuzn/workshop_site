from rest_framework import viewsets
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import DjangoModelPermissions, AllowAny, IsAuthenticated

from apps.orders import models 
from apps.orders.serializers import order_serializers as order_serializers
from apps.orders.serializers.machinetype_serializers import MachineTypeSerializer
from apps.orders.serializers.brand_serializers import MarkSerializer
from apps.orders.serializers.street_serializers import StreetSerializer
from apps.orders.serializers.settlement_serizlizers import SettlementSerializer
from apps.common.permissions import IsDispatcherOrReadOnly, GroupBasedPermissions
from apps.common.roles import Roles

class BrandViewSet(viewsets.ModelViewSet):
    queryset = models.machine.Brand.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [AllowAny]#[DjangoModelPermissions, IsDispatcherOrReadOnly]

class MachineTypeViewSet(viewsets.ModelViewSet):
    queryset = models.machine.MachineType.objects.all()
    serializer_class = MachineTypeSerializer
    permission_classes = [AllowAny]#[DjangoModelPermissions, IsDispatcherOrReadOnly]

class StreetViewSet(viewsets.ModelViewSet):
    queryset = models.address.Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [AllowAny]#[DjangoModelPermissions, IsDispatcherOrReadOnly]

class SettlementViewSet(viewsets.ModelViewSet):
    queryset = models.address.Settlement.objects.all()
    serializer_class = SettlementSerializer
    permission_classes = [AllowAny]#[DjangoModelPermissions, IsDispatcherOrReadOnly]
