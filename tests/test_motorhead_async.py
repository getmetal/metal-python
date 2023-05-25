import pytest
import httpx
from asynctest import CoroutineMock
from src.metal_sdk.motorhead_async import Motorhead


@pytest.mark.asyncio
async def test_initialization():
    m = Motorhead(api_key='test_key', client_id='test_client')
    assert m.api_key == 'test_key'
    assert m.client_id == 'test_client'

    with pytest.raises(ValueError):
        m = Motorhead()


@pytest.mark.asyncio
async def test_add_memory():
    async with httpx.AsyncClient(transport=httpx.MockTransport(add_memory_mock)) as client:
        m = Motorhead(api_key='test_key', client_id='test_client')
        m.client = client

        memory = await m.add_memory('test_session', {'key': 'value'})
        assert memory == 'mock_memory'


@pytest.mark.asyncio
async def test_get_memory():
    async with httpx.AsyncClient(transport=httpx.MockTransport(get_memory_mock)) as client:
        m = Motorhead(api_key='test_key', client_id='test_client')
        m.client = client

        memory = await m.get_memory('test_session')
        assert memory == 'mock_memory'


@pytest.mark.asyncio
async def test_delete_memory():
    async with httpx.AsyncClient(transport=httpx.MockTransport(delete_memory_mock)) as client:
        m = Motorhead(api_key='test_key', client_id='test_client')
        m.client = client

        memory = await m.delete_memory('test_session')
        assert memory == 'mock_memory'


async def add_memory_mock(request):
    return httpx.Response(200, json={'data': 'mock_memory'})


async def get_memory_mock(request):
    return httpx.Response(200, json={'data': 'mock_memory'})


async def delete_memory_mock(request):
    return httpx.Response(200, json={'data': 'mock_memory'})
