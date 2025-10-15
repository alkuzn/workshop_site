from django.shortcuts import render
from login import views
# Create your views here.
from django.http import HttpRequest
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def login_page(request: HttpRequest):
    auth_form = AuthenticationForm(data=request.POST or None)
    if request.user.is_active:
        return HttpResponsePermanentRedirect(reverse("common:about_page"))
    if request.method == 'POST':
        if auth_form.is_valid():
            user = authenticate(request, **auth_form.cleaned_data)
            login(request, user)    
            return HttpResponsePermanentRedirect(reverse("common:about_page"))
    return render(request, 'login.html', context={'login_form': auth_form})

def logout_e(request: HttpRequest):
    logout(request)
    return HttpResponsePermanentRedirect(reverse("login_page"))