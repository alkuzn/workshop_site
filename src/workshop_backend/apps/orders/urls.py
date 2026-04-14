from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from apps.orders.views import BrandViewSet, MachineTypeViewSet, StreetViewSet, SettlementViewSet, OrdersViewSet

router = DefaultRouter()
#router.register(r'orders/(?P<role>(dispatcher|manager|client|repairman))/orders', OrdersViewSet, 'orders')
router.register(r'order', OrdersViewSet, 'order')
router.register(r'machine-type', MachineTypeViewSet)
router.register(r'brand', BrandViewSet, 'brand')
router.register(r'street', StreetViewSet)
router.register(r'settlement', SettlementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
