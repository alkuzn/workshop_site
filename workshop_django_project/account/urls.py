from django.urls import path
from account import views

#app_name = 'account'
urlpatterns = [
    path('account/', views.account, name='account_page'),
    path('employee_page_choise/', views.employee_page_choise, name='employee_page_choise'),
]