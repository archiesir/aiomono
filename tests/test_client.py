import pytest
from aiomono.client import MonoClient
from unittest.mock import AsyncMock

@pytest.fixture
def mono_client():
    return MonoClient()


@pytest.mark.asyncio
async def test_get_currency(mono_client: MonoClient):
    async with mono_client as mono_client:
        mono_client.get = AsyncMock()
        mono_client.__check_response = AsyncMock()
        await mono_client.get_currency()
        mono_client.get.assert_called_once_with("/bank/currency")
