from django.db.models import TextChoices

class PaymentLocaleEnum(TextChoices):
    VIE = "vn"
    EN = "en"