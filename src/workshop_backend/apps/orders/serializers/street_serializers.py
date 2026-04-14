from rest_framework import serializers

from apps.orders.models.address import Street

class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = "__all__"