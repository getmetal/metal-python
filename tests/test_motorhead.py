import pytest
from httpx import Response
from unittest.mock import MagicMock
from src.metal_sdk.motorhead import Motorhead


def test_initialization():
    m = Motorhead(api_key='test_key', client_id='test_client')
    assert m.api_key == 'test_key'
    assert m.client_id == 'test_client'

    with pytest.raises(ValueError):
        m = Motorhead()


def test_add_memory():
    m = Motorhead(api_key='test_key', client_id='test_client')

    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {'data': 'mock_memory'}
    m.client.post = MagicMock(return_value=mock_response)

    memory = m.add_memory('test_session', {'key': 'value'})
    assert memory == 'mock_memory'
    m.client.post.assert_called_once_with(
      'https://api.getmetal.io/v1/motorhead/sessions/test_session/memory',
      json={'key': 'value'}
    )


def test_get_memory():
    m = Motorhead(api_key='test_key', client_id='test_client')

    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {'data': 'mock_memory'}
    m.client.get = MagicMock(return_value=mock_response)

    memory = m.get_memory('test_session')
    assert memory == 'mock_memory'
    m.client.get.assert_called_once_with('https://api.getmetal.io/v1/motorhead/sessions/test_session/memory')


def test_delete_memory():
    m = Motorhead(api_key='test_key', client_id='test_client')

    mock_response = MagicMock(spec=Response)
    mock_response.json.return_value = {'data': 'mock_memory'}
    m.client.delete = MagicMock(return_value=mock_response)

    memory = m.delete_memory('test_session')
    assert memory == 'mock_memory'
    m.client.delete.assert_called_once_with('https://api.getmetal.io/v1/motorhead/sessions/test_session/memory')
