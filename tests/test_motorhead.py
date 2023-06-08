import unittest
import respx
from httpx import Response
from unittest.mock import MagicMock
from src.metal_sdk.motorhead import Motorhead


class TestMotorhead(unittest.TestCase):
    def test_initialization(self):
        with self.assertRaises(ValueError) as ctx:
            Motorhead()
        self.assertEqual(str(ctx.exception), "api_key and client_id required for managed motorhead")

    @respx.mock
    def test_request(self):
        url = 'https://test_base_url/test_endpoint'
        method = 'GET'
        respx.get(url).mock(return_value=Response(200))

        payload = {"api_key": "test_key", "client_id": "test_id", "base_url": "https://test_base_url"}
        motorhead = Motorhead(payload)

        response = motorhead.request(method, "/test_endpoint")
        assert response.status_code == 200

    def test_add_memory(self):
        motorhead = Motorhead({"api_key": "test_key", "client_id": "test_client"})
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {'data': 'mock_memory'}
        motorhead.request = MagicMock(return_value=mock_response)

        memory = motorhead.add_memory('test_session', {'key': 'value'})
        self.assertEqual(memory, 'mock_memory')
        self.assertEqual(motorhead.request.call_count, 1)
        self.assertEqual(
            motorhead.request.call_args[0][0],
            "post",
        )
        self.assertEqual(
            motorhead.request.call_args[0][1],
            "/sessions/test_session/memory",
        )
        self.assertEqual(motorhead.request.call_args[1]["json"], {'key': 'value'})

    def test_get_memory(self):
        motorhead = Motorhead({"api_key": "test_key", "client_id": "test_client"})
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {'data': 'mock_memory'}
        motorhead.request = MagicMock(return_value=mock_response)

        memory = motorhead.get_memory('test_session')
        self.assertEqual(memory, 'mock_memory')
        self.assertEqual(motorhead.request.call_count, 1)
        self.assertEqual(
            motorhead.request.call_args[0][0],
            "get",
        )
        self.assertEqual(
            motorhead.request.call_args[0][1],
            "/sessions/test_session/memory",
        )

    def test_delete_memory(self):
        motorhead = Motorhead({"api_key": "test_key", "client_id": "test_client"})
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {'data': 'mock_memory'}
        motorhead.request = MagicMock(return_value=mock_response)

        memory = motorhead.delete_memory('test_session')
        self.assertEqual(memory, 'mock_memory')
        self.assertEqual(motorhead.request.call_count, 1)
        self.assertEqual(
            motorhead.request.call_args[0][0],
            "delete",
        )
        self.assertEqual(
            motorhead.request.call_args[0][1],
            "/sessions/test_session/memory",
        )
