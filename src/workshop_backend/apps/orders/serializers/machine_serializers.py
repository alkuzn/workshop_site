import logging

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.orders.models.machine import Machine, Brand, MachineType

logger = logging.getLogger(__name__)

class MachineSerializer(ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'
        #exclude = ('id', )
        
class MachineSerializerCreate(ModelSerializer):
    typeid = serializers.PrimaryKeyRelatedField(source="type", queryset=MachineType.objects)
    markid = serializers.PrimaryKeyRelatedField(source="mark", queryset=Brand.objects)

    def create(self, validated_data):
        machine,is_created = Machine.objects.get_or_create(**validated_data)#пока так. изменить!
        logger.error("MachineSerializerCreate: ИЗМЕНИТЬ КОСЯК")

        if is_created:
            logger.info(f'MachineSerializerCreate: cоздан объект - {machine}')
        return machine
        return super().create(validated_data)

    class Meta:
        model = Machine
        fields = ('typeid', 'markid', 'serial_number', 'model')
        extra_args = {
            ""
        }

class MachineSerializerView(ModelSerializer):
    type = serializers.StringRelatedField()
    mark = serializers.StringRelatedField()

    class Meta:
        model = Machine
        exclude = ('id', )
