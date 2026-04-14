from django.shortcuts import render

from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.request import Request
from rest_framework.response import Response

def index(request):
    return render(request, "index.html")

def contacts(request):
    return render(request, "contacts.html")

def about(request):
    return render(request, "about.html")

@api_view(["GET"])
@throttle_classes([UserRateThrottle])
def healthcheck(request: Request):
    #Тут проверка бд
    #кто дёргает, права
    return Response(data={'status': 'OK'}, status=200)