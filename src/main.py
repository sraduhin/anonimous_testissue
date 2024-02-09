import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.v1 import order
from core import config
from core.logger import LOGGING

# from db import elastic, redis


app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESC,
    version=config.PROJECT_VERSION,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


app.include_router(order.router, prefix="/api/v1/order", tags=["Заказы"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
