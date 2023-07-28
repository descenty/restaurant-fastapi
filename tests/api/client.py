from httpx import AsyncClient
from main import app


def get_async_client():
    return AsyncClient(app=app, base_url="http://test/api/v1")
