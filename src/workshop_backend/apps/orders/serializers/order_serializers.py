from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.orders.models import address
from apps.orders.models import machine
from apps.orders.models import order
from apps.orders.serializers.machine_serializers import MachineSerializerView, MachineSerializer, MachineSerializerCreate

class OrderSerializerCreate(ModelSerializer): 
    machine = MachineSerializerCreate()
    status = serializers.HiddenField(default=serializers.CreateOnlyDefault(order.OrderStatus.objects.first))#или из базы выбирать?
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    streetid = serializers.PrimaryKeyRelatedField(source='street', queryset=address.Street.objects, write_only=True)
    settlementid = serializers.PrimaryKeyRelatedField(source='settlement', queryset=address.Settlement.objects, write_only=True)
    
    def create(self, validated_data):
        machine_data = validated_data.pop('machine')
        validated_data['machine'], is_created = machine.Machine.objects.get_or_create(**machine_data)#Возникает ошибка. если указать не все данные, то находит много записей. Пока оставил так.
        return super().create(validated_data)

    class Meta:
        model = order.Order
        fields = ('machine', 'streetid', 'settlementid', 'building', 'appartment', 'additional_contacts', 'client', 'creator', 'status', 'problem', 'complekt')
        extra_kwargs = {
            'serial_number': {
                'default': ''
            },
            'model': {
                'default': ''
            },
        }

class OrderSerializerView(ModelSerializer):
    machine = MachineSerializerView()
    client = serializers.StringRelatedField()
    creator = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    street = serializers.StringRelatedField()
    settlement = serializers.StringRelatedField()
    class Meta:
        model = order.Order
        fields = "__all__"

class OrderSerializerViewDispatcher(OrderSerializerView):
    class Meta:
        model = order.Order
        fields = "__all__"

class OrderSerializerViewRepairman(OrderSerializerView):
    class Meta:
        model = order.Order
        fields = "__all__"
        #read_only_fields = [field.name for field in order_models.Order._meta.fields if field.name not in ["status"]]

class OrderSerializerViewClient(OrderSerializerView):
    class Meta:
        model = order.Order
        exclude = ("creator", 'repairman')

class OrderShortSerializer(OrderSerializerView):
    class Meta:
        model = order.Order
        fields = ['problem']

class OrderSerializerViewDetails(OrderSerializerView):
    class Meta:
        model = order.Order
        fields = "__all__"

class OrderSerializerUpdate(OrderSerializerCreate):
    machine = MachineSerializerCreate()#Такой сериализатор должен быть или другой?

    def update(self, instance, validated_data):
        machine_data = validated_data.pop('machine')
        validated_data['machine'], is_created = machine.Machine.objects.get_or_create(**machine_data)##ИЗМЕНИТЬ!Потом не вспомнишь, что это так работает
        return super().update(instance, validated_data)
    
    class Meta:
        model = order.Order
        fields = ('machine', 'streetid', 'settlementid', 'building', 'appartment', 'additional_contacts', 'complekt', 'problem', 'client')

