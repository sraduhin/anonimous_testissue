from typing import Annotated

from fastapi import APIRouter, Depends
from services.order import FileService
from dependencies.dep import get_payment_service, get_order_service

from fastapi import UploadFile

router = APIRouter()


@router.post(
    "/load_files/",
    summary="Файлы заказа",
    description="Загрузите файлы для формирования заказа. Поддерживаемые типы: .xml, .json",
    response_description="Данные по заказу",
)
async def load_files(
    order: UploadFile,
    payment: UploadFile,
    order_service: Annotated[FileService, Depends(get_order_service)],
    payment_service: Annotated[FileService, Depends(get_payment_service)],
):
    order = await order_service.read_file(order)
    payment = await payment_service.read_file(payment)
    return order.dump(payment)
