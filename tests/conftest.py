from httpx import AsyncClient
import pytest
from main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test/api/v1") as client:
        yield client
