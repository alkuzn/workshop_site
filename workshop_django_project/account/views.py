from django.shortcuts import render
from django.urls import reverse
from dispatcher import views as dviews
from django.http import HttpResponsePermanentRedirect
# Create your views here.

def account(request):
    return render(request, "profile.html")

def employee_page_choise(request):
    return HttpResponsePermanentRedirect(reverse("dispatcher_mainpage"))
    match ():
        case "dispatcher": return render(request, reverse(dviews.dispatcher_view))