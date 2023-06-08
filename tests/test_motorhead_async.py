import respx
from httpx import Response
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

    @respx.mock
    async def test_request(self):
        url = 'https://test_base_url/test_endpoint'
        method = 'GET'
        respx.get(url).mock(return_value=Response(200))

        payload = {"api_key": "test_key", "client_id": "test_id", "base_url": "https://test_base_url"}
        motorhead = Motorhead(payload)

        response = await motorhead.request(method, "/test_endpoint")
        assert response.status_code == 200

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
