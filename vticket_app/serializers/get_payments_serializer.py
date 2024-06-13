from rest_framework import serializers

class GetPaymentsSerializer(serializers.Serializer):
    payment_ids = serializers.ListField(child=serializers.IntegerField())