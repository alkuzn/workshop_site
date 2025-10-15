from rest_framework.serializers import ModelSerializer
from parts.models import Part, PartRequest

class PartSerializer(ModelSerializer):
    class Meta:
        model = Part
        fields = "__all__"

class PartRequestSerializer(ModelSerializer):
    class Meta:
        model = PartRequest
        fields = "__all__"