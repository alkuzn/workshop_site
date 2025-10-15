from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.serializers import Serializer

from orders import models 
from orders import serializers as order_serializers
from orders.permissions import IsRepairmanOwnerOrReadOnly, IsDispatcherOrReadOnly
from orders.roles import Roles

class MarkViewSet(viewsets.ModelViewSet):
    queryset = models.Mark.objects.all()
    serializer_class = order_serializers.MarkSerializer
    permission_classes = [DjangoModelPermissions, IsDispatcherOrReadOnly]

class MachineTypeViewSet(viewsets.ModelViewSet):
    queryset = models.MachineType.objects.all()
    serializer_class = order_serializers.MachineTypeSerializer
    permission_classes = [DjangoModelPermissions, IsDispatcherOrReadOnly]

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = order_serializers.OrderShortSerializer
    permission_classes = [DjangoModelPermissions, IsDispatcherOrReadOnly]
    
    def get_serializer_class(self):
        user_groups = self.request.user.groups.values_list("name", flat=True)#Переделать
        serializer_class = None
        
        match(self.request.method):
            case "POST": 
                serializer_class = order_serializers.NewOrderSerializer
            case ("PUT"|"PATCH"): 
                serializer_class = order_serializers.UpdateOrderSerializer
            case "GET" if Roles.dispatcher.value in user_groups: 
                serializer_class = order_serializers.DispatcherSerializer
            case "GET" if Roles.repairman.value in user_groups: 
                serializer_class = order_serializers.RepairmanSerializer
            case "GET" if Roles.client.value in user_groups: 
                serializer_class = order_serializers.ClientOrderSerializer
            case _ : serializer_class = super().get_serializer_class()
        print(self.request.method, user_groups)
        return serializer_class

    def get_queryset(self):
        user_id = self.request.user.id
        user_groups = self.request.user.groups.values_list("name", flat=True)
        filter = {}
        if Roles.repairman.value in user_groups:
            filter["repairman__id"] = user_id
        elif Roles.client.value in user_groups:
            filter["client__id"] = user_id
        if filter:
            return models.Order.objects.filter(**filter)
        else:
            return super().get_queryset()
    
    def perform_create(self, serializer: Serializer):
        serializer.save(dispatcher=self.request.user,
                        date_incomming=datetime.now(),
                        status=models.OrderStatus.objects.first()#Тут может быть проблема, когда база не заполнена статусами, нужно что-то придумать
                        )
    
    def perform_update(self, serializer):
        #Если поле заявка оплачена, то изменять её нельзяу
        return super().perform_update(serializer)

class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = order_serializers.JobViewSerializer
    permission_classes = [DjangoModelPermissions, IsRepairmanOwnerOrReadOnly]

    def get_serializer_class(self):
        serializer_class = None
        match(self.request.method):
            case "GET": 
                serializer_class = order_serializers.JobViewSerializer
            case ("POST"|"PUT"|"PATCH"): 
                serializer_class = order_serializers.JobSerializer
            case _: 
                serializer_class = super().get_serializer_class()
        return serializer_class

    def get_queryset(self):
        params = {
            "order_id": self.kwargs['order_id'], 
        }            
        return self.queryset.filter(**params)

    def perform_create(self, serializer: order_serializers.JobSerializer):
        params = {
            "repairman": self.request.user,
            'date_begin': datetime.now(),
            "order_id": self.kwargs['order_id'],
            "job_status": models.JobStatus.objects.first(),
        }
        serializer.save(**params)
    
    def perform_update(self, serializer):
        if serializer.validated_data['job_status'].name=='Готово':#Для теста. Не должно быть возможности менять статусы руками?
            serializer.save(date_end=datetime.now())
        return super().perform_update(serializer)

class ServiceCallViewSet(viewsets.ModelViewSet):
    queryset = models.ServiceCall.objects.all()
    serializer_class = order_serializers.ServiceCallViewSerializer
    permission_classes = [DjangoModelPermissions, IsDispatcherOrReadOnly]
    
    def get_queryset(self):
        params = {
            "order_id": self.kwargs['order_id'], 
        }            
        return self.queryset.filter(**params)
    
    def perform_create(self, serializer):
        params = {
            "dispatcher": self.request.user,
            "order_id": self.kwargs['order_id']#Или безопаснее объект заказа получить?
        }
        serializer.save(**params)

    def get_serializer_class(self):
        serializer_class = None
        match(self.request.method):
            case "GET": 
                serializer_class = order_serializers.ServiceCallViewSerializer
            case ("POST"|"PUT"|"PATCH"): 
                serializer_class = order_serializers.ServiceCallSerializer
            case _: 
                serializer_class = super().get_serializer_class()
        return serializer_class

from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
@api_view(["GET"])
@throttle_classes([UserRateThrottle])#А надо ли тут лимитирование?
def healthcheck(request: Request):
    return Response(status=200)

###################################################

from rest_framework import serializers

class SS(serializers.Serializer):
    file = serializers.FileField()

class Pipka(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()

class MachineFoto(views.APIView):#А нужен ли?
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAdminUser]
    
    def get(self, request: Request, order_id, file_name=None, format=None):
        from django.http.response import FileResponse
        import os
        p=Pipka(data=request.query_params)
        #print(request.headers)
        print(request.headers['cookie'])
        if p.is_valid():
            print(p.validated_data)
        if not file_name:
            return Response(data={"files": os.listdir(f"files_for_orders/{order_id}")})
        else:
            print(os.path.isfile(f'files_for_orders/{order_id}/{file_name}'))
            return FileResponse(open(f'files_for_orders/{order_id}/{file_name}', 'rb'))
        
    def post(self, request: Request, order_id, format=None):
        from rest_framework.serializers import FileField
        t=SS(data=request.data)
        t.is_valid()
        #request.data['file']
        #InMemoryUploadedFile из from django.core.files.uploadedfile
        #имя файла должно быть хешем
        
        with open(f"files_for_orders/{order_id}/{t.validated_data['file'].name}", 'wb') as file:
            file.write(t.validated_data['file'].file.read())
        print(t.validated_data)

        return Response(t.validated_data['file'])