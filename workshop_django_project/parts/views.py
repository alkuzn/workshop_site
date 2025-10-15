from django.shortcuts import render
from rest_framework import viewsets
from parts.models import PartRequest, Part
from parts.serializers import PartSerializer, PartRequestSerializer
# Create your views here.

class PartViewset(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    #permission_classes = []
    
