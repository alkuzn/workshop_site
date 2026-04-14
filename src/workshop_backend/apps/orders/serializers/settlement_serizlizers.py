from rest_framework import serializers

from apps.orders.models.address import Settlement

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = "__all__"