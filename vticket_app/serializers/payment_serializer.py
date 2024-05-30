from rest_framework import serializers

from vticket_app.models.payment import Payment
from vticket_app.models.payment_request import PaymentRequest

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        existing = set(self.fields.keys())
        fields = kwargs.pop("fields", []) or existing
        exclude = kwargs.pop("exclude", [])
        
        super().__init__(*args, **kwargs)
        
        for field in exclude + list(existing - fields):
            self.fields.pop(field, None)

    payment_request = serializers.PrimaryKeyRelatedField(queryset=PaymentRequest.objects.all(), many=False, allow_null=False)
    pay_date = serializers.DateTimeField(input_formats=["%Y%m%d%H%M%S"])

    __mapping_key_obj = {
        "vnp_Amount": "amount",
        "vnp_BankCode": "bank_code",
        "vnp_BankTranNo": "bank_tran_no",
        "vnp_CardType": "card_type",
        "vnp_PayDate": "pay_date",
        "vnp_OrderInfo": "order_info",
        "vnp_TransactionNo": "tran_no",
        "vnp_ResponseCode": "response_code",
        "vnp_TransactionStatus": "transaction_status",
        "vnp_TxnRef": "payment_request",
        "vnp_SecureHashType": "secure_hash_type",
        "vnp_SecureHash": "secure_hash"
    }

    __mapping_data_type_obj = {
        "amount": lambda x: int(x),
        "tran_no": lambda x: int(x),
        "response_code": lambda x: int(x),
        "transaction_status": lambda x: int(x)
    }

    @staticmethod
    def mapping(data):
        __mapped_data = {}

        for bk, ak in PaymentSerializer.__mapping_key_obj.items():
            if bk in data:
                __mapped_data[ak] = data[bk]

        for k, exp in PaymentSerializer.__mapping_data_type_obj.items():
            __mapped_data[k] = exp(__mapped_data[k])

        return __mapped_data