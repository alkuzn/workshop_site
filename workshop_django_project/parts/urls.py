from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parts.views import PartViewset

router = DefaultRouter()
router.register(r"parts", PartViewset)

urlpatterns = [
    path("", include(router.urls))
]