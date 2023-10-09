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

    async def test_metal_index_many_with_indexid(self):
        my_index = "my-index"
        mock_text = "some text"
        mock_id = "some-id"
        mock_metadata = {"some": "metadata"}

        payload = [{"id": mock_id, "text": mock_text, "metadata": mock_metadata}]
        payload_with_index = [{"id": mock_id, "text": mock_text, "metadata": mock_metadata, "index": my_index}]

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
        self.assertEqual(metal.request.call_args[1]["json"]["data"], payload_with_index)

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

    async def test_metal_get_many_with_payload(self):
        index_id = "index-id"
        ids = ["dave", "ozzy"]
        metal = Metal(API_KEY, CLIENT_ID, index_id)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "foo"}

        metal.request = mock.AsyncMock(return_value=mock_response)

        await metal.get_many(ids)
        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "get")
        self.assertEqual(metal.request.call_args[0][1], "/v1/indexes/index-id/documents/dave,ozzy")

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

        res = await metal.upload_file(mock_file_path)

        self.assertEqual(res['data']['url'], 'https://mockuploadurl.com')

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

    async def test_metal_add_datasource_with_payload(self):
        my_datasource = "my_datasource"
        mock_metadata = [{"name": "some-name", "type": "string", "description": "some-description"}]
        mock_sourcetype = "file"
        mock_auto_extract = True
        payload = {
            "name": my_datasource,
            "metadataFields": mock_metadata,
            "sourcetype": mock_sourcetype,
            "autoExtract": mock_auto_extract
        }

        metal = Metal(API_KEY, CLIENT_ID)
        metal.request = mock.AsyncMock(return_value=mock.Mock(status_code=201))
        await metal.add_datasource(payload)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "post")
        self.assertEqual(metal.request.call_args[0][1], "/v1/datasources")
        self.assertEqual(metal.request.call_args[1]["json"]["name"], my_datasource)
        self.assertEqual(metal.request.call_args[1]["json"]["metadataFields"], payload["metadataFields"])

    async def test_get_datasource_with_payload(self):
        id = "datasource-id"
        metal = Metal(API_KEY, CLIENT_ID)
        return_value = mock.MagicMock(json=lambda: {"datasource": "sample data"})
        metal.request = mock.AsyncMock(return_value=return_value)

        result = await metal.get_datasource(id)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "get")
        self.assertEqual(metal.request.call_args[0][1], "/v1/datasources/datasource-id")
        self.assertEqual(result, return_value.json())

    async def test_get_datasource_without_payload(self):
        metal = Metal(API_KEY, CLIENT_ID)

        with self.assertRaises(TypeError) as ctx:
            await metal.get_datasource(None)

        self.assertEqual(str(ctx.exception), "datasource_id required")

    async def test_update_datasource_with_payload(self):
        datasource_id = "datasource-id"
        mock_name = "updated-datasource-name"
        mock_metadata = [{"name": "updated-name", "type": "string", "description": "updated-description"}]
        payload = {
            "name": mock_name,
            "metadataFields": mock_metadata,
        }

        metal = Metal(API_KEY, CLIENT_ID)
        return_value = mock.MagicMock(json=lambda: {"updated": True})
        metal.request = mock.AsyncMock(return_value=return_value)

        res = await metal.update_datasource(datasource_id, payload)

        self.assertEqual(res['updated'], True)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "put")
        self.assertEqual(metal.request.call_args[0][1], f"/v1/datasources/{datasource_id}")
        self.assertEqual(metal.request.call_args[1]["json"]["name"], mock_name)
        self.assertEqual(metal.request.call_args[1]["json"]["metadataFields"], mock_metadata)

    async def test_add_data_entity(self):
        datasource_id = "datasource-id"

        # Get the directory containing this file
        this_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the path to the CSV file
        mock_file_path = os.path.join(this_dir, 'fixtures', 'sample.csv')

        metal = Metal(API_KEY, CLIENT_ID)

        metal._Metal__add_data_entity_resource = mock.AsyncMock(return_value={
            'data': {'url': 'https://mockuploadurl.com'}
            })
        metal._Metal__upload_file_to_url = mock.AsyncMock()

        res = await metal.add_data_entity(datasource_id, mock_file_path)

        self.assertEqual(res['data']['url'], 'https://mockuploadurl.com')

        self.assertEqual(metal._Metal__add_data_entity_resource.call_count, 1)
        self.assertEqual(metal._Metal__upload_file_to_url.call_count, 1)

        create_args = metal._Metal__add_data_entity_resource.call_args[0]
        self.assertEqual(create_args[0], datasource_id)
        self.assertEqual(create_args[1], "sample.csv")
        self.assertEqual(create_args[2], 47)
        upload_args = metal._Metal__upload_file_to_url.call_args[0]
        self.assertEqual(upload_args[0], 'https://mockuploadurl.com')
        self.assertEqual(upload_args[1], mock_file_path)
        self.assertEqual(upload_args[2], "text/csv")
        self.assertEqual(upload_args[3], 47)

    async def test_metal_get_data_entity_with_id(self):
        data_entity_id = "data_entity-id"
        mock_return_value = {"data": "sample response"}

        metal = Metal(API_KEY, CLIENT_ID)
        return_value = mock.MagicMock(json=lambda: mock_return_value)
        metal.request = mock.AsyncMock(return_value=return_value)

        await metal.get_data_entity(data_entity_id)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "get")
        self.assertEqual(metal.request.call_args[0][1], f"/v1/data-entities/{data_entity_id}")

    async def test_metal_delete_data_entity_with_id(self):
        data_entity_id = "data_entity-id"

        metal = Metal(API_KEY, CLIENT_ID)
        return_value = mock.MagicMock(status_code=204)
        metal.request = mock.AsyncMock(return_value=return_value)

        await metal.delete_data_entity(data_entity_id)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "delete")
        self.assertEqual(metal.request.call_args[0][1], f"/v1/data-entities/{data_entity_id}")

    async def test_metal_get_all_data_entities_with_datasource_id(self):
        datasource_id = "datasource-id"
        mock_limit = 10
        mock_page = 2
        metal = Metal(API_KEY, CLIENT_ID)
        return_value = mock.MagicMock(json=lambda: {
            "data": [
                {"id": "data_entity-1", "name": "Entity 1"},
                {"id": "data_entity-2", "name": "Entity 2"},
                ]
        })
        metal.request = mock.AsyncMock(return_value=return_value)

        await metal.get_all_data_entities(datasource_id, limit=mock_limit, page=mock_page)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "get")
        self.assertEqual(metal.request.call_args[0][1], f"/v1/datasources/{datasource_id}/data-entities")
        self.assertDictEqual(metal.request.call_args[1]["params"], {"limit": mock_limit, "page": mock_page})

    async def test_metal_add_index_with_payload(self):
        mock_index_name = "test_index"
        mock_datasource = "test_datasource"
        mock_model = "test_model"
        mock_filters = [{"field": "test_field", "operator": "equals", "value": "test_value"}]

        payload = {
            "model": mock_model,
            "datasource": mock_datasource,
            "name": mock_index_name,
            "filters": mock_filters
        }

        metal = Metal(API_KEY, CLIENT_ID)
        metal.request = mock.AsyncMock(return_value=mock.Mock(status_code=201))
        await metal.add_index(payload)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "post")
        self.assertEqual(metal.request.call_args[0][1], "v1/indexes")
        self.assertEqual(metal.request.call_args[1]["json"]["name"], mock_index_name)
        self.assertEqual(metal.request.call_args[1]["json"]["datasource"], mock_datasource)
        self.assertEqual(metal.request.call_args[1]["json"]["model"], mock_model)
        self.assertEqual(metal.request.call_args[1]["json"]["filters"], mock_filters)

    async def test_metal_update_index_with_payload(self):
        mock_index_id = "test_index"

        payload = {
            "status": "UNARCHIVED",
        }

        metal = Metal(API_KEY, CLIENT_ID)
        metal.request = mock.AsyncMock(return_value=mock.Mock(status_code=200))
        await metal.update_index(mock_index_id, payload)

        self.assertEqual(metal.request.call_count, 1)
        self.assertEqual(metal.request.call_args[0][0], "put")
        self.assertEqual(metal.request.call_args[0][1], "v1/indexes/test_index")
        self.assertEqual(metal.request.call_args[1]["json"]["status"], "UNARCHIVED")
