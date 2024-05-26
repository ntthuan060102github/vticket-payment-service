from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from vticket_app.decorators.validate_body import validate_body
from vticket_app.dtos.payment_request_dto import PaymentRequestDTO
from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.serializers.payment_request_serializer import PaymentRequestSerializer
from vticket_app.services.payment_service import PaymentService
from vticket_app.utils.response import RestResponse

class PaymentView(viewsets.ViewSet):
    payment_service = PaymentService()

    @action(methods=["POST"], detail=False, url_path="pay-url")
    @swagger_auto_schema(request_body=PaymentRequestSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    @validate_body(PaymentRequestSerializer)
    def get_payment_url(self, request: Request, validated_body: dict):
        try:
            dto = PaymentRequestDTO(**validated_body)
            url = self.payment_service.get_payment_url(dto)
            return RestResponse().success().set_data({"url": url}).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response

    @action(methods=["GET"], detail=False, url_path="IPN", authentication_classes=())
    def IPN(self, request: Request):
        return Response(data={"RspCode": "00", "Message": "Confirm Success"})