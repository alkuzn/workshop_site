from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission

from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status

from orders import models
from orders.roles import Roles

class AccountTests(APITestCase):
    def setUp(self):
        models.Settlement.objects.bulk_create([
            models.Settlement(name="Балахна"),
            models.Settlement(name="Богородск")
        ])
        models.Street.objects.bulk_create([
            models.Street(name="Коминтерна", city=models.Settlement.objects.get(id=1)),
            models.Street(name="Бийская", city=models.Settlement.objects.get(id=2))
        ])
        models.MachineType.objects.bulk_create([
            models.MachineType(type_name="Стиральная машина"),
            models.MachineType(type_name="Телевизор")
        ])
        models.Mark.objects.bulk_create([
            models.Mark(name="Samsung"),
            models.Mark(name="LG"),
            models.Mark(name="Xiaomi")
        ])
        models.Machine.objects.bulk_create([
            models.Machine(type=models.MachineType.objects.get(id=1),
                           mark=models.Mark.objects.get(id=1),
                           model="90LOP"),
            models.Machine(type=models.MachineType.objects.get(id=2),
                           mark=models.Mark.objects.get(id=2),
                           model="43LOP")
        ])
        
        #Group.objects.bulk_create([
        #    Group(name=Roles.dispatcher.value),
        #    Group(name=Roles.repairman.value),
        #])
        User.objects.bulk_create([
            User(username=f'alex_{Roles.dispatcher.value}'),
            User(username=f'alex_{Roles.repairman.value}')
        ])
        User.objects.get(id=1).groups.set([Group.objects.get(name=Roles.dispatcher.value)])
        User.objects.get(id=2).groups.set(Group.objects.filter(name=Roles.repairman.value))
        models.OrderStatus.objects.create(name="Создан")
        models.ServiceCallType.objects.create(
            name="Выезд"
        )
        return super().setUp()
    
    def test_create_mark(self):
        """
        Проверяем можно ли добавлять новые марки
        """
        url = reverse('mark-list')
        data = {
            "name": "Trololo-Brand"
        }
        Group.objects.get(name=Roles.dispatcher.value).permissions.add(*Permission.objects.filter(codename='add_mark'))
        self.client.force_login(User.objects.filter(groups__name=Roles.dispatcher.value).first())
        response = self.client.post(url, data, format='json')
        
        self.assertTrue(models.Mark.objects.filter(name=data['name']).exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_with_minimum_data(self):
        """
        Убеждаемся Что можем создать заявку с минимальным количеством данных
        """
        url = reverse('orders-list')
        data = {
            "machine": {
                "type": 1,
                "mark": 3,
            },
            "service_call":{
                "type": 1,
                "visit_datetime": "2025-12-19T15:26",
                "repairman": 1
            },
            "problem": "Не робит",
            "building": "2",
            "repairman": 1,
            "client": 1,
            "settlement": 1,
        }
        Group.objects.get(name=Roles.dispatcher.value).permissions.add(*Permission.objects.filter(codename='add_order'))
        self.client.force_login(User.objects.filter(groups__name=Roles.dispatcher.value).first())
        response = self.client.post(url, data, format='json')
        print(response.json())
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_service_call(self):
        url = reverse('servicecall-list', kwargs={'order_id':1})
        order = models.Order.objects.create(
            machine=models.Machine.objects.first(),
            problem="Не робит",
            building="2",
            status=models.OrderStatus.objects.first(),
            dispatcher=User.objects.first(),
            repairman=User.objects.first(),
            client=User.objects.first(),
            settlement=models.Settlement.objects.first(),
        )
        data = {
            "visit_datetime": "2025-12-19T15:26",
            "type": 1,
            "note": "ff",
            "repairman": 1,
            "dispatcher": 1,
            "order": 1
        }
        Group.objects.get(name=Roles.dispatcher.value).permissions.add(*Permission.objects.filter(codename='add_servicecall'))
        self.client.force_login(User.objects.filter(groups__name=Roles.dispatcher.value).first())
        response = self.client.post(url, data, format='json')
        print(response.json())
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_file(self):
        #from django.core.files.uploadedfile import SimpleUploadedFile
        #test_file = SimpleUploadedFile(
        #    name='test_image.jpg',
        #    content=b'This is a dummy file.',
        #    content_type='image/jpeg'
        #)
#
        ## Отправляем POST-запрос с файлом
        #response = self.client.post('/api/upload/', {'file_field': test_file}, format='multipart')
        
        ff = ""
        with open('manage.py','rb') as file:
            #Е
            response = self.client.post("/orders/1/files", {"file": file}, format="multipart")
        print(response.text)
        