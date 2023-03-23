from unittest import TestCase, mock
from src.metal.metal import Metal


API_KEY = "api-key"
CLIENT_ID = "client-id"


class TestMetal(TestCase):
    def test_metal_instantiate(self):
        app_id = "app-id"
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        self.assertEqual(metal.api_key, API_KEY)
        self.assertEqual(metal.client_id, CLIENT_ID)
        self.assertEqual(metal.app_id, app_id)

    def test_metal_get_headers(self):
        metal = Metal(API_KEY, CLIENT_ID)
        headers = metal._Metal__get_headers()
        self.assertEqual(headers["x-metal-api-key"], API_KEY)
        self.assertEqual(headers["x-metal-client-id"], CLIENT_ID)

    def test_metal_index_without_app(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            metal.index()
        self.assertEqual(str(ctx.exception), "app_id required")

    def test_metal_index_without_payload(self):
        my_app = "my-app"
        metal = Metal(API_KEY, CLIENT_ID, my_app)

        with self.assertRaises(TypeError) as ctx:
            metal.index()
        self.assertEqual(
            str(ctx.exception), "imageBase64, imageUrl, text, or embedding required"
        )

    def test_metal_index_with_text(self):
        my_app = "my-app"
        mock_text = "some text"
        mock_id = "some-id"
        payload = {"id": mock_id, "text": mock_text}

        metal = Metal(API_KEY, CLIENT_ID, my_app)
        metal.request = mock.MagicMock(return_value=mock.Mock(status_code=201))
        metal.index(payload)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(
            metal.request.call_args[0][0], "post"
        )
        self.assertEqual(
            metal.request.call_args[0][1], "/index"
        )
        self.assertEqual(metal.request.call_args[1]["json"]["app"], my_app)
        self.assertEqual(metal.request.call_args[1]["json"]["text"], payload["text"])

    def test_metal_search_without_app(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            metal.search()
        self.assertEqual(str(ctx.exception), "app_id required")

    def test_metal_search_without_payload(self):
        my_app = "my-app"
        metal = Metal(API_KEY, CLIENT_ID, my_app)

        with self.assertRaises(TypeError) as ctx:
            metal.search()
        self.assertEqual(
            str(ctx.exception), "imageBase64, imageUrl, text, or embedding required"
        )

    def test_metal_search_with_text(self):
        my_app = "my-app"
        payload = {"text": "some text"}

        metal = Metal(API_KEY, CLIENT_ID, my_app)

        metal.request = mock.MagicMock(return_value=mock.Mock(status_code=201))

        metal.search(payload, ids_only=True)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(
            metal.request.call_args[0][0],
            "post",
        )
        self.assertEqual(
            metal.request.call_args[0][1],
            "/search?idsOnly=true",
        )
        self.assertEqual(metal.request.call_args[1]["json"]["app"], my_app)
        self.assertEqual(metal.request.call_args[1]["json"]["text"], payload["text"])

    def test_metal_tune_without_app(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            metal.tune()
        self.assertEqual(str(ctx.exception), "app_id required")

    def test_metal_tune_witout_payload(self):
        app_id = "app-id"
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        with self.assertRaises(TypeError) as ctx:
            metal.tune()
        self.assertEqual(str(ctx.exception), "idA, idB, and label required")

    def test_metal_tune_with_payload(self):
        app_id = "app-id"
        payload = {"idA": "id-a", "idB": "id-b", "label": -1}
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        return_value = mock.MagicMock(json=lambda: {"status": "success", "message": "ok"})
        metal.request = mock.MagicMock(return_value=return_value)

        metal.tune(payload)
        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "post")
        self.assertEqual(metal.request.call_args[0][1], "/tune")
        self.assertEqual(metal.request.call_args[1]["json"]["app"], app_id)
        self.assertEqual(metal.request.call_args[1]["json"]["idA"], payload["idA"])
        self.assertEqual(metal.request.call_args[1]["json"]["idB"], payload["idB"])
        self.assertEqual(metal.request.call_args[1]["json"]["label"], payload["label"])
