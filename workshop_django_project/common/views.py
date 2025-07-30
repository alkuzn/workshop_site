from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import os
# Create your views here.
def index(request):
    return render(request, "index.html")

def contacts(request):
    return render(request, "contacts.html")

def about(request):
    return render(request, "about.html")
