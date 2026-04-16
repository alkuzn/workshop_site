from rest_framework.serializers import ModelSerializer

from apps.orders.models.machine import Brand

class MarkSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

