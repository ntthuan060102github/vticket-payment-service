from rest_framework import serializers

from vticket_app.models.payment_request import PaymentRequest

class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = "__all__"
        read_only_fields = ("id",)