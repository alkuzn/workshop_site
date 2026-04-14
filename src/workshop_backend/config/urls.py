from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from apps.common import urls as common_urls
from apps.orders import urls as orders_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(common_urls, namespace='common')),
    path('', include(orders_urls)),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from rest_framework import urls as rest_login_urls

    urlpatterns += [ 
        path("rest_login/", include(rest_login_urls)),
    ] + debug_toolbar_urls()
