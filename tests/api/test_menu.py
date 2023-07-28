import pytest
from tests.api.client import get_async_client


@pytest.mark.anyio
async def test_get_all():
    async with get_async_client() as ac:
        response = await ac.get("menus")
    assert response.status_code == 200
