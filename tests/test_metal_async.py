from unittest import TestCase, mock
from src.metal_sdk.metal_async import Metal


API_KEY = "api-key"
CLIENT_ID = "client-id"


class TestMetal(TestCase):
    def test_metal_instantiate(self):
        app_id = "app-id"
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        self.assertEqual(metal.api_key, API_KEY)
        self.assertEqual(metal.client_id, CLIENT_ID)
        self.assertEqual(metal.app_id, app_id)

    async def test_metal_index_without_app(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            await metal.index()
        self.assertEqual(str(ctx.exception), "app_id required")

    async def test_metal_index_without_payload(self):
        my_app = "my-app"
        metal = Metal(API_KEY, CLIENT_ID, my_app)

        with self.assertRaises(TypeError) as ctx:
            await metal.index()
        self.assertEqual(
            str(ctx.exception), "imageBase64, imageUrl, text, or embedding required"
        )

    async def test_metal_index_with_text(self):
        my_app = "my-app"
        mock_text = "some text"
        mock_id = "some-id"
        mock_metadata = {"some": "metadata"}

        payload = {"id": mock_id, "text": mock_text, "metadata": mock_metadata}

        metal = Metal(API_KEY, CLIENT_ID, my_app)
        metal.request = mock.MagicMock(return_value=mock.Mock(status_code=201))
        await metal.index(payload)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(
            metal.request.call_args[0][0], "post"
        )
        self.assertEqual(
            metal.request.call_args[0][1], "/v1/index"
        )
        self.assertEqual(metal.request.call_args[1]["json"]["app"], my_app)
        self.assertEqual(metal.request.call_args[1]["json"]["text"], payload["text"])
        self.assertEqual(metal.request.call_args[1]["json"]["metadata"], payload["metadata"])

    async def test_metal_search_without_app(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            await metal.search()
        self.assertEqual(str(ctx.exception), "app_id required")

    async def test_metal_search_without_payload(self):
        my_app = "my-app"
        metal = Metal(API_KEY, CLIENT_ID, my_app)

        with self.assertRaises(TypeError) as ctx:
            await metal.search()
        self.assertEqual(
            str(ctx.exception), "imageBase64, imageUrl, text, or embedding required"
        )

    async def test_metal_search_with_text(self):
        my_app = "my-app"
        payload = {"text": "some text"}

        metal = Metal(API_KEY, CLIENT_ID, my_app)

        metal.request = mock.MagicMock(return_value=mock.Mock(status_code=201))

        await metal.search(payload, ids_only=True, limit=100)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(
            metal.request.call_args[0][0],
            "post",
        )
        self.assertEqual(
            metal.request.call_args[0][1],
            "/v1/search?limit=100&idsOnly=true",
        )
        self.assertEqual(metal.request.call_args[1]["json"]["app"], my_app)
        self.assertEqual(metal.request.call_args[1]["json"]["text"], payload["text"])

    async def test_metal_tune_without_app(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            await metal.tune()
        self.assertEqual(str(ctx.exception), "app_id required")

    async def test_metal_tune_witout_payload(self):
        app_id = "app-id"
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        with self.assertRaises(TypeError) as ctx:
            await metal.tune()
        self.assertEqual(str(ctx.exception), "idA, idB, and label required")

    async def test_metal_tune_with_payload(self):
        app_id = "app-id"
        payload = {"idA": "id-a", "idB": "id-b", "label": -1}
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        return_value = mock.MagicMock(json=lambda: {"status": "success", "message": "ok"})
        metal.request = mock.MagicMock(return_value=return_value)

        await metal.tune(payload)
        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "post")
        self.assertEqual(metal.request.call_args[0][1], "/v1/tune")
        self.assertEqual(metal.request.call_args[1]["json"]["app"], app_id)
        self.assertEqual(metal.request.call_args[1]["json"]["idA"], payload["idA"])
        self.assertEqual(metal.request.call_args[1]["json"]["idB"], payload["idB"])
        self.assertEqual(metal.request.call_args[1]["json"]["label"], payload["label"])

    async def test_metal_get_one_with_payload(self):
        app_id = "app-id"
        id = "dave"
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        return_value = mock.MagicMock(json=lambda: {"band": "Megadeth"})
        metal.request = mock.MagicMock(return_value=return_value)

        await metal.get_one(id)
        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "get")
        self.assertEqual(metal.request.call_args[0][1], "/v1/documents/dave")

    async def test_metal_delete_one_with_payload(self):
        app_id = "app-id"
        id = "dave"
        metal = Metal(API_KEY, CLIENT_ID, app_id)
        return_value = mock.MagicMock(json=lambda: {"band": "Megadeth"})
        metal.request = mock.MagicMock(return_value=return_value)

        await metal.get_one(id)
        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "delete")
        self.assertEqual(metal.request.call_args[0][1], "/v1/documents/dave")
