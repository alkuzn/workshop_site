from django.urls import path
from login import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('logout', views.logout_e, name='logout'),
]