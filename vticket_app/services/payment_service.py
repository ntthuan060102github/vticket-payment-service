import urllib.parse
from uuid import uuid4
from django.conf import settings
import urllib

from vticket_app.dtos.payment_request_dto import PaymentRequestDTO
from vticket_app.helpers.vnpay import vnpay

class PaymentService():
    __terminal_id = settings.PAYMENT_TERMINAL_ID
    __hash_secret = settings.PAYMENT_HASH_SECRET
    __base_url = settings.PAYMENT_URL
    __version = settings.PAYMENT_VERSION
    __pay_command = settings.PAYMENT_PAY_COMMAMD

    def get_payment_url(self, data: PaymentRequestDTO) -> str:
        vnp = vnpay()

        vnpay.requestData = {
            "vnp_Version": self.__version,
            "vnp_Command": self.__pay_command,
            "vnp_TmnCode": self.__terminal_id,
            "vnp_Amount": data.amount*100,
            "vnp_CreateDate": data.created_date.strftime("%Y%m%d%H%M%S"),
            "vnp_CurrCode": "VND",
            "vnp_IpAddr": data.customer_ip,
            "vnp_Locale": data.locale,
            "vnp_OrderInfo": data.order_info,
            "vnp_OrderType": "other",
            "vnp_ReturnUrl": "https://vticket.netlify.app/",
            "vnp_ExpireDate": data.expire_date.strftime("%Y%m%d%H%M%S"),
            "vnp_TxnRef": uuid4().hex
        }
        
        return vnp.get_payment_url(self.__base_url, self.__hash_secret)