from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.orders.models.machine import MachineType

class MachineTypeSerializer(ModelSerializer):
    class Meta:
        model = MachineType
        fields = "__all__"