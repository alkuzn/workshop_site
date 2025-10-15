from django.urls import path, include,re_path

from rest_framework.routers import DefaultRouter
from rest_framework import urls

from orders.views import OrdersViewSet, JobViewSet, ServiceCallViewSet, MarkViewSet, MachineTypeViewSet,MachineFoto, healthcheck

router = DefaultRouter()
router.register(r'orders', OrdersViewSet, 'orders')
router.register(r'orders/(?P<order_id>[^/.]+)/jobs', JobViewSet, "order-jobs")
router.register(r'orders/(?P<order_id>[^/.]+)/service-calls', ServiceCallViewSet)
router.register(r'machine-types', MachineTypeViewSet)
router.register(r'mark', MarkViewSet, 'mark')


urlpatterns = [
    path('', include(router.urls)),
    re_path('orders/(?P<order_id>[^/.]+)/files/(?P<file_name>[^/.]+)',MachineFoto.as_view()),
    re_path('orders/(?P<order_id>[^/.]+)/files',MachineFoto.as_view()),
    #path('orders/shortinfo/<int:pk>', ShortOrderInfoView.as_view()),
    path('healthcheck/', healthcheck),
    path("tt/", include(urls)),
]
