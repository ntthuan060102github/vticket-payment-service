from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

from vticket_app.enums.payment_locale_enum import PaymentLocaleEnum

class PaymentRequest(models.Model):
    class Meta:
        db_table = "payment_request"
    
    id = models.UUIDField(primary_key=True)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    created_date = models.DateTimeField(null=False)
    customer_ip = models.GenericIPAddressField(null=False)
    locale = models.CharField(max_length=10, choices=PaymentLocaleEnum.choices, default=PaymentLocaleEnum.VIE)
    order_info = models.CharField(max_length=255, validators=[RegexValidator("[a-zA-z0-9\s]*")])
    expire_date = models.DateTimeField(null=False)