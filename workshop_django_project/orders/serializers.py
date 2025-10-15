from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from orders import models as order_models
#Я хотел получить список групп которые могут изменять поле и закэшировать его, а при изменении грпупп кеш сбрасывать
#Тип заказа: ожидает согласования времени


class ServiceCallSerializer(ModelSerializer):
    class Meta:
        model = order_models.ServiceCall
        exclude = ["order", ]
        read_only_fields = ["dispatcher",]

class ServiceCallViewSerializer(ModelSerializer):
    type = serializers.StringRelatedField()
    class Meta:
        model = order_models.ServiceCall
        exclude = ["order", ]
        read_only_fields = ["dispatcher",]

class OrderSerializer(ModelSerializer):
    class Meta:
        model = order_models.Order
        fields = '__all__'

class MarkSerializer(ModelSerializer):
    class Meta:
        model = order_models.Mark
        fields = "__all__"

class MachineTypeSerializer(ModelSerializer):
    class Meta:
        model = order_models.MachineType
        fields = "__all__"

class MachineSerializer(ModelSerializer):
    class Meta:
        model = order_models.Machine
        fields = "__all__"
        #extra_kwargs = {'password': {'write_only': True}}

class MachineViewSerializer(ModelSerializer):
    type = serializers.CharField(source="type.type_name", read_only=True)
    mark = serializers.CharField(source="mark.name", read_only=True)
    #def to_internal_value(self, data):
    #    return self.queryset.get(id=data)
    class Meta:
        model = order_models.Machine
        exclude = ('id',)

class NewOrderSerializer(OrderSerializer):
    service_call = ServiceCallSerializer(required=False)
    machine = MachineSerializer()

    def create(self, validated_data:dict):#Это должна быть транзакция?
        machine_data = validated_data.pop('machine')
        service_call_data = validated_data.pop('service_call', None)
        validated_data['machine'], is_created = order_models.Machine.objects.get_or_create(**machine_data)
        print(service_call_data)
        new_order = super().create(validated_data)
        if service_call_data:
            service_call_data['dispatcher'] = new_order.dispatcher
            new_order.servicecalls.create(**service_call_data)
        return new_order

    class Meta(OrderSerializer.Meta):
        fields = None
        exclude = ('date_incomming', 'date_begin', 'date_end', 'dispatcher', 'status')

class UpdateOrderSerializer(OrderSerializer):
    machine = MachineSerializer()

    def update(self, instance, validated_data):
        machine_data = validated_data.pop('machine')
        validated_data['machine'], is_created = order_models.Machine.objects.get_or_create(**machine_data)
        return super().update(instance, validated_data)

    class Meta(OrderSerializer.Meta):
        #exclude = ('date_incomming', 'date_begin', 'date_end', 'dispatcher', 'status')
        read_only_fields = ('date_incomming', 'date_begin', 'date_end', 'dispatcher', 'status')

class OrderViewSerializer(OrderSerializer):
    machine = MachineViewSerializer()
    client = serializers.StringRelatedField()
    dispatcher = serializers.StringRelatedField()
    repairman = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    street = serializers.StringRelatedField()
    settlement = serializers.StringRelatedField()

    class Meta(OrderSerializer.Meta):
        pass

class ClientOrderSerializer(OrderViewSerializer):
    class Meta(OrderSerializer.Meta):
        fields = None
        exclude = ("dispatcher", 'repairman')

class SupplyOrderSerializer(OrderViewSerializer):
    class Meta(OrderSerializer.Meta):
        fields = ('id', 'repairman', 'dispatcher', 'machine')

class UserSerializator(OrderViewSerializer):
    class Meta(OrderSerializer.Meta):
        fields = ('username', 'id', )

class DispatcherSerializer(OrderViewSerializer):
    dispatcher = serializers.StringRelatedField()
    repairman = serializers.StringRelatedField()
    class Meta(OrderSerializer.Meta):
        read_only_fields = ('date_incomming', 'date_begin', 'date_end', 'dispatcher', 'status')

class RepairmanSerializer(OrderViewSerializer):
    dispatcher = serializers.StringRelatedField()
    repairman = serializers.StringRelatedField()
    class Meta(OrderSerializer.Meta):
        read_only_fields = [field.name for field in order_models.Order._meta.fields if field.name not in ["status"]]

class OrderShortSerializer(ModelSerializer):
    class Meta:
        model = order_models.Order
        fields = ['problem']

class JobSerializer(ModelSerializer):

    def update(self, instance, validated_data):
        if instance.paid_date:
            from rest_framework.response import Response
            return Response('Невозможно изменить оплаченную работу', status=403)
        return super().update(instance, validated_data)

    class Meta:
        model = order_models.Job
        fields = "__all__"
        read_only_fields = ("repairman", 'date_begin', 'date_end', 'order')

class JobViewSerializer(ModelSerializer):
    class Meta:
        model = order_models.Job
        fields = "__all__"
        read_only_fields = ("repairman", 'date_begin', 'date_end', 'order')


##Для теста. удали потом. Было лень припрятывать
from rest_framework import serializers
class Hyper(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(
    #    view_name='accounts',
    #    lookup_field='slug'
    #)
    class Meta:
        model = order_models.Order
        fields = '__all__' 

class ListingField(serializers.RelatedField):
    def __init__(self, *args, ftv:list[str],  **kwargs):
        super().__init__(*args, **kwargs)
        self.fields_to_view = ftv

    def to_representation(self, value):
        result = ""
        for field_name in self.fields_to_view:
            if hasattr(value, field_name):
                result = f"{result} {getattr(value, field_name)}"
            else:
                raise AttributeError(f"Нету татрибута {field_name}")
        return result
    
    def to_internal_value(self, data):
        return self.queryset.get(id=data)
