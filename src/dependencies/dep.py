from services.order import FileService
from utils.parser import (
    JSONOrderValidator,
    JSONPaymentValidator,
    XMLOrderValidator,
    XMLPaymentValidator,
)


def get_order_service():
    return FileService(JSONOrderValidator, XMLOrderValidator)


def get_payment_service():
    return FileService(JSONPaymentValidator, XMLPaymentValidator)
