"""
URL configuration for workshop_django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from common import urls as common_urls
from login import urls as login_urls
from account import urls as account_urls
from dispatcher import urls as dispatcher_urls
from orders import urls as orders_urls
from parts import urls as parts_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(common_urls, namespace='common')),
    path('auth/',include(login_urls)),
    path('', include(account_urls)),
    path('employee-panel/', include(dispatcher_urls)),
    path('', include(orders_urls)),
    path('', include(parts_urls))
]

