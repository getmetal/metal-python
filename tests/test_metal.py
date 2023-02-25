import unittest
from src.metal_sdk.metal import Metal


API_KEY = 'api-key'
CLIENT_ID = 'client-id'

class TestMetal(unittest.TestCase):
    def test_metal_instantiate(self):
        app_id = 'app-id'
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        self.assertEqual(metal.apiKey, API_KEY)
        self.assertEqual(metal.clientId, CLIENT_ID)
        self.assertEqual(metal.appId, 'app_id')