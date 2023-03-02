from unittest import TestCase, mock
from src.metal_sdk.Metal import Metal


API_KEY = 'api-key'
CLIENT_ID = 'client-id'

class TestMetal(TestCase):
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
    
    # @mock.patch('requests.post', return_value=mock.Mock(status_code=200, json=mock.Mock(return_value={'error': 'App ID is required.'}))
    @mock.patch('requests.post')
    def test_metal_index_without_app(self, mocked_post):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            metal.index()
        self.assertEqual(str(ctx.exception), 'app_id required')
    
    @mock.patch('requests.post')
    def test_metal_index_without_payload(self, mocked_post):
        my_app = 'my-app'
        metal = Metal(API_KEY, CLIENT_ID, my_app)
        
        with self.assertRaises(TypeError) as ctx:
            metal.index()
        self.assertEqual(str(ctx.exception), 'imageBase64, imageUrl, text, or embedding required')
    
    @mock.patch('requests.post')
    def test_metal_index_with_text(self, mocked_post):
        my_app = 'my-app'
        payload = { 'text': 'some text' }

        mocked_post.return_value = mock.Mock(status_code=201)

        metal = Metal(API_KEY, CLIENT_ID, my_app)
        metal.index(payload)

        self.assertEqual(mocked_post.call_count, 1)
        self.assertEqual(mocked_post.call_args[0][0], 'https://api.getmetal.io/v1/index')
        self.assertEqual(mocked_post.call_args[1]['json']['app'], my_app)
        self.assertEqual(mocked_post.call_args[1]['json']['text'], payload['text'])
    
    @mock.patch('requests.post')
    def test_metal_search_without_app(self, mocked_post):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            metal.search()
        self.assertEqual(str(ctx.exception), 'app_id required')
    
    @mock.patch('requests.post')
    def test_metal_search_without_payload(self, mocked_post):
        my_app = 'my-app'
        metal = Metal(API_KEY, CLIENT_ID, my_app)
        
        with self.assertRaises(TypeError) as ctx:
            metal.search()
        self.assertEqual(str(ctx.exception), 'imageBase64, imageUrl, text, or embedding required')
    
    @mock.patch('requests.post')
    def test_metal_search_with_text(self, mocked_post):
        my_app = 'my-app'
        payload = { 'text': 'some text' }

        mocked_post.return_value = mock.Mock(status_code=201)

        metal = Metal(API_KEY, CLIENT_ID, my_app)
        metal.search(payload)

        self.assertEqual(mocked_post.call_count, 1)
        self.assertEqual(mocked_post.call_args[0][0], 'https://api.getmetal.io/v1/search')
        self.assertEqual(mocked_post.call_args[1]['json']['app'], my_app)
        self.assertEqual(mocked_post.call_args[1]['json']['text'], payload['text'])

    @mock.patch('requests.post')
    def test_metal_tune_without_app(self, mocked_post):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            metal.tune()
        self.assertEqual(str(ctx.exception), 'app_id required')

    @mock.patch('requests.post')
    def test_metal_tune_witout_payload(self, mocked_post):
        app_id = 'app-id'
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        with self.assertRaises(TypeError) as ctx:
            metal.tune()
        self.assertEqual(str(ctx.exception), 'idA, idB, and label required')

    @mock.patch('requests.post')
    def test_metal_tune_with_payload(self, mocked_post):
        app_id = 'app-id'
        payload = {
            'idA': 'id-a',
            'idB': 'id-b',
            'label': -1
        }
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        metal.tune(payload)

        self.assertEqual(mocked_post.call_count, 1)
        self.assertEqual(mocked_post.call_args[0][0], 'https://api.getmetal.io/v1/apps/app-id/tunings')
        self.assertEqual(mocked_post.call_args[1]['json']['idA'], payload['idA'])
        self.assertEqual(mocked_post.call_args[1]['json']['idB'], payload['idB'])
        self.assertEqual(mocked_post.call_args[1]['json']['label'], payload['label'])
