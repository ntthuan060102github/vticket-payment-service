from dataclasses import dataclass
from datetime import datetime

@dataclass
class PaymentRequestDTO():
    amount: int = None
    order_id: int = None
    created_date: datetime = None
    customer_ip: str = ""
    locale: str = ""
    order_info: str = ""
    expire_date: datetime = None