import unittest
from httpx import Response
from unittest.mock import MagicMock
from src.metal_sdk.motorhead import Motorhead

class TestMotorhead(unittest.TestCase):

    def setUp(self):
        self.motorhead = Motorhead(api_key='test_key', client_id='test_client')

    def test_initialization(self):
        self.assertEqual(self.motorhead.api_key, 'test_key')
        self.assertEqual(self.motorhead.client_id, 'test_client')

        with self.assertRaises(ValueError):
            Motorhead()

    def test_add_memory(self):
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {'data': 'mock_memory'}
        self.motorhead.client.post = MagicMock(return_value=mock_response)

        memory = self.motorhead.add_memory('test_session', {'key': 'value'})
        self.assertEqual(memory, 'mock_memory')
        self.motorhead.client.post.assert_called_once_with(
          'https://api.getmetal.io/v1/motorhead/sessions/test_session/memory',
          json={'key': 'value'}
        )

    def test_get_memory(self):
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {'data': 'mock_memory'}
        self.motorhead.client.get = MagicMock(return_value=mock_response)

        memory = self.motorhead.get_memory('test_session')
        self.assertEqual(memory, 'mock_memory')
        self.motorhead.client.get.assert_called_once_with('https://api.getmetal.io/v1/motorhead/sessions/test_session/memory')

    def test_delete_memory(self):
        mock_response = MagicMock(spec=Response)
        mock_response.json.return_value = {'data': 'mock_memory'}
        self.motorhead.client.delete = MagicMock(return_value=mock_response)

        memory = self.motorhead.delete_memory('test_session')
        self.assertEqual(memory, 'mock_memory')
        self.motorhead.client.delete.assert_called_once_with('https://api.getmetal.io/v1/motorhead/sessions/test_session/memory')
