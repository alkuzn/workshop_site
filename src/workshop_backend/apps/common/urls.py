from django.urls import path, re_path

from apps.common import views

app_name='common'

urlpatterns = [
    #path('', views.index),
    #path('contacts/', views.contacts, name='contacts_page'),
    #path('about/', views.about, name='about_page'),
    re_path('health/', views.healthcheck)
]