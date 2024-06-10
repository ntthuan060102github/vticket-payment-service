from rest_framework import serializers

from vticket_app.models.payment import Payment

class RefundSerializer(serializers.Serializer):
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.filter(refund_at=None))
    user_id = serializers.IntegerField()