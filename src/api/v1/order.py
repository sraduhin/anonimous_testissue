from typing import Annotated

import fastapi
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

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
    return JSONResponse(
        status_code=fastapi.status.HTTP_200_OK, content=order.dump(payment)
    )
