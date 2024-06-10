import hashlib
import hmac
import json
import socket
import pytz
import requests
from uuid import uuid4
from datetime import datetime
from django.conf import settings
from dataclasses import asdict

from vticket_app.configs.related_service import RelatedService
from vticket_app.models.payment import Payment
from vticket_app.models.payment_request import PaymentRequest
from vticket_app.dtos.payment_request_dto import PaymentRequestDTO
from vticket_app.helpers.vnpay import vnpay

class PaymentService():
    __terminal_id = settings.PAYMENT_TERMINAL_ID
    __hash_secret = settings.PAYMENT_HASH_SECRET
    __base_url = settings.PAYMENT_URL
    __refund_url = settings.PAYMENT_REFUND_URL
    __version = settings.PAYMENT_VERSION
    __pay_command = settings.PAYMENT_PAY_COMMAMD
    __refund_command = settings.PAYMENT_REFUND_COMMAMD

    def get_payment_url(self, data: PaymentRequestDTO) -> str:
        vnp = vnpay()
        _req_id = uuid4().hex

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
            "vnp_ReturnUrl": "https://vticket.netlify.app/payment-result",
            "vnp_ExpireDate": data.expire_date.strftime("%Y%m%d%H%M%S"),
            "vnp_TxnRef": _req_id
        }

        self.__save_payment_request(data, _req_id)
        
        return vnp.get_payment_url(self.__base_url, self.__hash_secret)
    
    def __save_payment_request(self, data: PaymentRequestDTO, id: str) -> bool:
        try:
            instance = PaymentRequest(
                **{
                    "id": id,
                    **asdict(data)
                }
            )
            instance.save()
            return True
        except Exception as e:
            print(e)
            return False

    def update_payement(self, data: dict) -> bool:
        try:
            instance = Payment(**data)
            instance.save()

            if instance.transaction_status == 0:
                return self.update_order(instance.payment_request.order_id, instance.pay_date, instance.id)
            else:
                return True
        except Exception as e:
            print(e)
            return False
        
    def update_order(self, order_id: str, paid_at: datetime, payment_id: int) -> bool:
        try:
            resp = requests.post(
                url=f"{RelatedService.event}/ticket/update",
                data=json.dumps(
                    {
                        "booking_id": order_id,
                        "paid_at": paid_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "payment_id": payment_id
                    }
                ),
                headers={
                    "Content-type": "application/json"
                }
            )
            resp_data = resp.json()
            print(resp_data)
            return resp_data["status"] == 1
        except Exception as e:
            print(e)
            return False
        
    def get_payment_by_id(self, payment_id: int) -> Payment | None:
        try:
            return Payment.objects.get(id=payment_id)
        except Exception as e:
            print(e)
            return False
        
    def refund(self, user_id: int, payment: Payment) -> bool:
        try:
            data = {
                "vnp_RequestId": uuid4().hex,
                "vnp_Version": self.__version,
                "vnp_Command": self.__refund_command,
                "vnp_TmnCode": self.__terminal_id,
                "vnp_TransactionType": "02",
                "vnp_TxnRef": payment.payment_request.id.hex,
                "vnp_Amount": int(payment.amount/100),
                "vnp_TransactionNo": payment.tran_no,
                "vnp_TransactionDate": payment.pay_date.strftime("%Y%m%d%H%M%S"),
                "vnp_CreateBy": f"user_{user_id}",
                "vnp_CreateDate": datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%Y%m%d%H%M%S"),
                "vnp_IpAddr": self.get_machine_ip(),
                "vnp_OrderInfo": f"Hoan_tien_don_hang_{payment.payment_request.id}"
            }

            pre_checksum_data = "|".join([str(v) for v in data.values()])
            secure_hash = hmac.new(self.__hash_secret.encode(), pre_checksum_data.encode(), hashlib.sha512).hexdigest()
            data["vnp_SecureHash"] = secure_hash
            resp = requests.post(
                url=self.__refund_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
            resp_data = resp.json()

            return resp_data["vnp_ResponseCode"] == "00"
        except Exception as e:
            print(e)
            return False

    def __hash_with_secure_type(self, secret_key: str, data: str) -> str:
        return vnpay._vnpay__hmacsha512(secret_key, data=data)
    
    def get_machine_ip(self):
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            print(e)
            return None