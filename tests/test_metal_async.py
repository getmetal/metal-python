import os
import respx
from httpx import Response
from unittest import IsolatedAsyncioTestCase, mock
from src.metal_sdk.metal_async import Metal


API_KEY = "api-key"
CLIENT_ID = "client-id"


class TestMetal(IsolatedAsyncioTestCase):
    def test_metal_instantiate(self):
        index_id = "index-id"
        metal = Metal(API_KEY, CLIENT_ID, index_id)
        self.assertEqual(metal.api_key, API_KEY)
        self.assertEqual(metal.client_id, CLIENT_ID)
        self.assertEqual(metal.index_id, index_id)

    @respx.mock
    async def test_request(self):
        url = 'https://api.getmetal.io/foo/bar'
        method = 'GET'
        respx.get(url).mock(return_value=Response(200))

        index_id = "index-id"
        metal = Metal(API_KEY, CLIENT_ID, index_id)

        response = await metal.request(method, "/foo/bar")
        assert response.status_code == 200

    async def test_metal_index_without_index(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            await metal.index()
        self.assertEqual(str(ctx.exception), "index_id required")

    async def test_metal_index_without_payload(self):
        my_index = "my-index"
        metal = Metal(API_KEY, CLIENT_ID, my_index)

        with self.assertRaises(TypeError) as ctx:
            await metal.index()
        self.assertEqual(
            str(ctx.exception), "imageBase64, imageUrl, text, or embedding required"
        )

    async def test_metal_index_with_text(self):
        my_index = "my-index"
        mock_text = "some text"
        mock_id = "some-id"
        mock_metadata = {"some": "metadata"}

        payload = {"id": mock_id, "text": mock_text, "metadata": mock_metadata}

        metal = Metal(API_KEY, CLIENT_ID, my_index)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)
        await metal.index(payload)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(
            metal.request.call_args[0][0], "post"
        )
        self.assertEqual(
            metal.request.call_args[0][1], "/v1/index"
        )
        self.assertEqual(metal.request.call_args[1]["json"]["index"], my_index)
        self.assertEqual(metal.request.call_args[1]["json"]["text"], payload["text"])
        self.assertEqual(metal.request.call_args[1]["json"]["metadata"], payload["metadata"])

    async def test_metal_index_many_with_text(self):
        my_index = "my-index"
        mock_text = "some text"
        mock_id = "some-id"
        mock_metadata = {"some": "metadata"}

        payload = [{"id": mock_id, "text": mock_text, "metadata": mock_metadata, "index": my_index}]

        metal = Metal(API_KEY, CLIENT_ID, my_index)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)
        await metal.index_many(payload)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(
            metal.request.call_args[0][0], "post"
        )
        self.assertEqual(
            metal.request.call_args[0][1], "/v1/index/bulk"
        )
        self.assertEqual(metal.request.call_args[1]["json"]["data"], payload)

    async def test_metal_search_without_index(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            await metal.search()
        self.assertEqual(str(ctx.exception), "index_id required")

    async def test_metal_search_without_payload(self):
        my_index = "my-index"
        metal = Metal(API_KEY, CLIENT_ID, my_index)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)

        await metal.search()

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(
            metal.request.call_args[0][0],
            "post",
        )
        self.assertEqual(
            metal.request.call_args[0][1],
            "/v1/search?limit=1",
        )
        self.assertEqual(metal.request.call_args[1]["json"]["index"], my_index)
        self.assertEqual(metal.request.call_args[1]["json"].get("text"), None)

    async def test_metal_search_with_text(self):
        my_index = "my-index"
        payload = {"text": "some text"}

        metal = Metal(API_KEY, CLIENT_ID, my_index)

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)

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
        self.assertEqual(metal.request.call_args[1]["json"]["index"], my_index)
        self.assertEqual(metal.request.call_args[1]["json"]["text"], payload["text"])

    async def test_metal_tune_without_index(self):
        metal = Metal(API_KEY, CLIENT_ID)
        with self.assertRaises(TypeError) as ctx:
            await metal.tune()
        self.assertEqual(str(ctx.exception), "index_id required")

    async def test_metal_tune_witout_payload(self):
        index_id = "index-id"
        metal = Metal(API_KEY, CLIENT_ID, index_id)
        with self.assertRaises(TypeError) as ctx:
            await metal.tune()
        self.assertEqual(str(ctx.exception), "idA, idB, and label required")

    async def test_metal_tune_with_payload(self):
        index_id = "index-id"
        payload = {"idA": "id-a", "idB": "id-b", "label": -1}
        metal = Metal(API_KEY, CLIENT_ID, index_id)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)

        await metal.tune(payload)
        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "post")
        self.assertEqual(metal.request.call_args[0][1], "/v1/tune")
        self.assertEqual(metal.request.call_args[1]["json"]["index"], index_id)
        self.assertEqual(metal.request.call_args[1]["json"]["idA"], payload["idA"])
        self.assertEqual(metal.request.call_args[1]["json"]["idB"], payload["idB"])
        self.assertEqual(metal.request.call_args[1]["json"]["label"], payload["label"])

    async def test_metal_get_one_with_payload(self):
        index_id = "index-id"
        id = "dave"
        metal = Metal(API_KEY, CLIENT_ID, index_id)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)

        await metal.get_one(id)
        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "get")
        self.assertEqual(metal.request.call_args[0][1], "/v1/indexes/index-id/documents/dave")

    async def test_metal_delete_one_with_payload(self):
        index_id = "index-id"
        id = "dave"
        metal = Metal(API_KEY, CLIENT_ID, index_id)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)

        await metal.delete_one(id)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "delete")
        self.assertEqual(metal.request.call_args[0][1], "/v1/indexes/index-id/documents/dave")

    async def test_metal_delete_many_with_payload(self):
        index_id = "index-id"
        id = "ozzy"
        metal = Metal(API_KEY, CLIENT_ID, index_id)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)

        await metal.delete_many([id])

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "delete")
        self.assertEqual(metal.request.call_args[0][1], "/v1/indexes/index-id/documents/bulk")
        self.assertEqual(metal.request.call_args[1]["json"]["ids"], [id])

    async def test_upload_file(self):
        my_index = "my-index"
        mock_file_path = "/path/to/mockfile.csv"

        metal = Metal(API_KEY, CLIENT_ID, my_index)

        metal._Metal__create_resource = mock.AsyncMock(return_value={'data': {'url': 'https://mockuploadurl.com'}})
        metal._Metal__upload_file_to_url = mock.AsyncMock()
        os.path.getsize = mock.MagicMock(return_value=1000)
        os.path.basename = mock.MagicMock(return_value="mockfile.csv")

        await metal.upload_file(mock_file_path)

        self.assertEqual(metal._Metal__create_resource.call_count, 1)
        self.assertEqual(metal._Metal__upload_file_to_url.call_count, 1)

        create_args = metal._Metal__create_resource.call_args[0]
        self.assertEqual(create_args[0], my_index)
        self.assertEqual(create_args[1], "mockfile.csv")
        self.assertEqual(create_args[2], "text/csv")
        self.assertEqual(create_args[3], 1000)

        upload_args = metal._Metal__upload_file_to_url.call_args[0]
        self.assertEqual(upload_args[0], 'https://mockuploadurl.com')
        self.assertEqual(upload_args[1], mock_file_path)
        self.assertEqual(upload_args[2], "text/csv")
        self.assertEqual(upload_args[3], 1000)
