import unittest
from src.metal_sdk.metal import Metal


API_KEY = 'api-key'
CLIENT_ID = 'client-id'

class TestMetal(unittest.TestCase):
    def test_metal_instantiate(self):
        app_id = 'app-id'
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        self.assertEqual(metal.api_key, API_KEY)
        self.assertEqual(metal.client_id, CLIENT_ID)
        self.assertEqual(metal.app_id, app_id)
    
    def test_metal_get_headers(self):
        metal = Metal(API_KEY, CLIENT_ID)
        headers = metal._Metal__get_headers()
        self.assertEqual(headers['x-metal-api-key'], API_KEY)
        self.assertEqual(headers['x-metal-client-id'], CLIENT_ID)