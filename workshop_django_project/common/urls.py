from django.urls import path
from common import views
app_name='common'
urlpatterns = [
    path('', views.index),
    path('contacts/', views.contacts, name='contacts_page'),
    path('about/', views.about, name='about_page'),
]