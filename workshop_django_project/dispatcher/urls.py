from django.urls import path
from dispatcher import views
urlpatterns = [
    path("", views.dispatcher_view, name="dispatcher_mainpage"),
    path("repairman/", views.repairman_view, name="repairman_view")
]