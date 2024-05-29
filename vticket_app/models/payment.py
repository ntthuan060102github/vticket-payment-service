from django.db import models
from django.core.validators import MinValueValidator

from vticket_app.models.payment_request import PaymentRequest

class Payment(models.Model):
    class Meta:
        db_table = "payment"
    
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    bank_code = models.CharField(max_length=50)
    bank_tran_no = models.CharField(max_length=150)
    card_type = models.CharField(max_length=50)
    pay_date = models.DateTimeField()
    order_info = models.CharField(max_length=255)
    tran_no = models.BigIntegerField()
    response_code = models.IntegerField()
    transaction_status = models.IntegerField()
    payment_request = models.OneToOneField(PaymentRequest, on_delete=models.CASCADE, related_name="payment")
    secure_hash_type = models.CharField(max_length=10)
    secure_hash = models.CharField(max_length=256)