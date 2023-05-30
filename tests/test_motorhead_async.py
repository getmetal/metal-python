from unittest import TestCase, mock
from src.metal_sdk.motorhead_async import Motorhead


API_KEY = "api-key"
CLIENT_ID = "client-id"


class TestMotorheadAsync(TestCase):
    async def test_initialization(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})
        self.assertEqual(m.api_key, API_KEY)
        self.assertEqual(m.client_id, CLIENT_ID)

        with self.assertRaises(ValueError):
            Motorhead()

    async def test_add_memory(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})
        m.client.post = mock.MagicMock(return_value=mock.Mock(status_code=201))

        memory = await m.add_memory('test_session', {'key': 'value'})
        self.assertEqual(memory, 'mock_memory')

    async def test_get_memory(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})
        m.client.get = mock.MagicMock(return_value=mock.Mock(status_code=200))

        memory = await m.get_memory('test_session')
        self.assertEqual(memory, 'mock_memory')

    async def test_delete_memory(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})
        m.client.delete = mock.MagicMock(return_value=mock.Mock(status_code=204))

        memory = await m.delete_memory('test_session')
        self.assertEqual(memory, 'mock_memory')
