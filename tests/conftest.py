import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient

import pytest
from fastapi.testclient import TestClient
from src.main import app



@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as a_client:
        yield a_client
