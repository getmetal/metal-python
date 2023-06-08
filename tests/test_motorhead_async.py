from unittest import IsolatedAsyncioTestCase, mock
from src.metal_sdk.motorhead_async import Motorhead


API_KEY = "api-key"
CLIENT_ID = "client-id"


class TestMotorheadAsync(IsolatedAsyncioTestCase):
    async def test_initialization(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})
        self.assertEqual(m.api_key, API_KEY)
        self.assertEqual(m.client_id, CLIENT_ID)

        with self.assertRaises(ValueError):
            Motorhead()

    async def test_add_memory(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "mock_memory"}

        m.request = mock.AsyncMock(return_value=mock_response)

        memory = await m.add_memory('test_session', {'key': 'value'})
        self.assertEqual(memory, 'mock_memory')
        self.assertEqual(m.request.call_count, 1)
        self.assertEqual(m.request.call_args[0][0], "post")
        self.assertEqual(m.request.call_args[0][1], "/sessions/test_session/memory")

    async def test_get_memory(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "mock_memory"}

        m.request = mock.AsyncMock(return_value=mock_response)

        memory = await m.get_memory('test_session')
        self.assertEqual(memory, 'mock_memory')
        self.assertEqual(m.request.call_count, 1)
        self.assertEqual(m.request.call_args[0][0], "get")
        self.assertEqual(m.request.call_args[0][1], "/sessions/test_session/memory")

    async def test_delete_memory(self):
        m = Motorhead({"api_key": API_KEY, "client_id": CLIENT_ID})
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "mock_memory"}

        m.request = mock.AsyncMock(return_value=mock.Mock(status_code=204))

        await m.delete_memory('test_session')

        self.assertEqual(m.request.call_count, 1)
        self.assertEqual(m.request.call_args[0][0], "delete")
        self.assertEqual(m.request.call_args[0][1], "/sessions/test_session/memory")
