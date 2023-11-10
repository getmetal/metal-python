import os
import mimetypes
from typing import List
import httpx
from .typings import (
    IndexPayload,
    SearchPayload,
    TunePayload,
    BulkIndexItem,
    DataSourcePayload,
    CreateIndexPayload,
    UpdateIndexPayload,
    CreateAppPayload,
    UpdateAppPayload,
)
import logging

BASE_API = "https://api.getmetal.io"
logger = logging.getLogger(__name__)


class Metal(httpx.AsyncClient):
    api_key: str
    client_id: str
    index_id: str

    def __init__(self, api_key, client_id, index_id=None, base_url=BASE_API, timeout=30.0):
        super().__init__(timeout=timeout)
        self.api_key = api_key
        self.client_id = client_id
        self.index_id = index_id
        self.headers.update({
            'Content-Type': 'application/json',
            'x-metal-api-key': self.api_key,
            'x-metal-client-id': self.client_id,
        })
        self.base_url = base_url

    async def request(self, method, url, *args, **kwargs):
        return await super().request(method, url, *args, **kwargs)

    def __getData(self, index, payload: dict = {}):
        data = {"index": index}
        if payload.get("id") is not None:
            data["id"] = payload["id"]

        if payload.get("metadata") is not None:
            data["metadata"] = payload["metadata"]

        if payload.get("filters") is not None:
            data["filters"] = payload["filters"]

        if payload.get("imageBase64") is not None:
            data["imageBase64"] = payload["imageBase64"]
        elif payload.get("imageUrl") is not None:
            data["imageUrl"] = payload["imageUrl"]
        elif payload.get("text") is not None:
            data["text"] = payload["text"]
        elif payload.get("embedding") is not None:
            data["embedding"] = payload["embedding"]

        return data

    def __validateIndex(self, index=None, payload={}):
        if index is None:
            raise TypeError("index_id required")

        if (
            payload.get("imageBase64") is None
            and payload.get("imageUrl") is None
            and payload.get("text") is None
            and payload.get("embedding") is None
        ):
            raise TypeError("imageBase64, imageUrl, text, or embedding required")

    async def fetch(self, method, url, data, params=None):
        try:
            res = await self.request(method, url, json=data, params=params)

            res.raise_for_status()
            if not res.content:
                return
            return res.json()
        except httpx.HTTPStatusError as e:
            response_data = e.response.text
            try:
                response_data = e.response.json()
            except Exception:
                pass

            status_code = e.response.status_code

            if isinstance(response_data, dict):
                error_detail = response_data.get('error', {})
                nested_message = error_detail.get('message') if isinstance(error_detail, dict) else None
                top_level_message = response_data.get('message')
                immediate_error = response_data.get('error')
            else:
                nested_message = None
                top_level_message = None
                immediate_error = None

            error_message = nested_message or top_level_message or immediate_error or f"HTTP {status_code} error"

            formatted_error = f"\n{'='*60}\nError occurred while accessing {url}: {error_message}\n{'='*60}\n"
            logger.exception(formatted_error)

            return response_data

    async def index(self, payload: IndexPayload = {}, index_id=None):
        index = self.index_id or index_id
        self.__validateIndex(index, payload)
        data = self.__getData(index, payload)
        url = "/v1/index"

        res = await self.fetch("post", url, data)
        return res

    async def index_many(self, payload: List[BulkIndexItem]):
        url = "/v1/index/bulk"

        for item in payload:
            if item.get("index") is None:
                item["index"] = self.index_id

        data = {"data": payload}
        res = await self.fetch("post", url, data)
        return res

    async def search(
        self, payload: SearchPayload = {}, index_id=None, ids_only=False, limit=1
    ):
        index = index_id or self.index_id

        if index is None:
            raise TypeError("index_id required")

        data = self.__getData(index, payload)

        url = "/v1/search?limit=" + str(limit)

        if ids_only:
            url = url + "&idsOnly=true"

        res = await self.fetch("post", url, data)
        return res

    async def tune(self, payload: TunePayload = {}, index_id=None):
        index = index_id or self.index_id

        if index is None:
            raise TypeError("index_id required")

        idA = payload.get("idA")
        idB = payload.get("idB")
        label = payload.get("label")

        if idA is None or idB is None or label is None:
            raise TypeError("idA, idB, and label required")

        url = "/v1/tune"
        data = {"index": index, "idA": idA, "idB": idB, "label": label}

        res = await self.fetch("post", url, data)
        return res

    async def get_one(self, id: str, index_id=None):
        index = index_id or self.index_id

        if id is None:
            raise TypeError("id required")

        if index is None:
            raise TypeError("index_id required")

        url = "/v1/indexes/" + index + "/documents/" + id

        res = await self.fetch("get", url, None)
        return res

    async def get_many(self, ids: List[str], index_id=None):
        index = index_id or self.index_id

        if not (1 < len(ids) <= 100):
            raise TypeError("ids should be between 1 and 100")

        if index is None:
            raise TypeError("index_id required")

        id_str = ",".join(ids)

        url = "/v1/indexes/" + index + "/documents/" + id_str

        res = await self.fetch("get", url, None)

        if isinstance(res, list):
            return res
        else:
            return [res]

    async def delete_one(self, id: str, index_id=None):
        index = index_id or self.index_id

        if id is None:
            raise TypeError("id required")

        if index is None:
            raise TypeError("index_id required")

        url = "/v1/indexes/" + index + "/documents/" + id

        res = await self.fetch("delete", url, None)
        return res

    async def delete_many(self, ids: List[str], index_id=None):
        index = index_id or self.index_id

        if index is None:
            raise TypeError("index_id required")

        if ids is None:
            raise TypeError("ids required")

        url = "/v1/indexes/" + index + "/documents/bulk"
        data = {"ids": ids}
        res = await self.fetch("delete", url, data)
        return res

    def __sanitize_filename(self, filename):
        """
        Implement your filename sanitation method here.
        """
        sanitized_filename = filename.replace(' ', '_')  # Simplified example
        return sanitized_filename

    async def __create_resource(self, index_id, filename, file_type, file_size):
        url = f'{self.base_url}/v1/indexes/{index_id}/files'
        payload = {
            'fileName': self.__sanitize_filename(filename),
            'fileType': file_type,
        }
        headers = {'x-metal-file-size': str(file_size)}

        res = await self.request("post", url, json=payload, headers=headers)
        res.raise_for_status()  # Raise exception if the request failed

        return res.json()

    async def __upload_file_to_url(self, url, file_path, file_type, file_size):
        with open(file_path, 'rb') as f:
            headers = {
                'content-type': file_type,
                'content-length': str(file_size),
            }
            res = await self.request("put", url, data=f, headers=headers)

        res.raise_for_status()  # Raise exception if the request failed
        return res

    async def upload_file(self, file_path, index_id=None):
        index = index_id or self.index_id

        if index is None:
            raise TypeError("index_id required")

        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        file_type, _ = mimetypes.guess_type(file_path)

        if file_type not in [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'text/csv',
        ]:
            raise ValueError("Invalid file type. Supported types are: pdf, docx, csv.")

        # Create resource on the server
        resource = await self.__create_resource(index, filename, file_type, file_size)

        # Upload the file to the returned url
        await self.__upload_file_to_url(resource['data']['url'], file_path, file_type, file_size)
        return resource

    async def add_datasource(self,  payload: DataSourcePayload = {}):
        url = "/v1/datasources"
        res = await self.fetch("post", url, payload)
        return res

    async def get_datasource(self, id: str):
        if id is None:
            raise TypeError("datasource_id required")

        url = f"/v1/datasources/{id}"
        res = await self.fetch("get", url, None)
        return res

    async def get_all_datasources(self, limit=None, page=None):
        url = "/v1/datasources"

        params = {}
        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page

        res = await self.fetch("get", url, params)
        return res

    async def delete_datasource(self, id: str):
        if id is None:
            raise TypeError("datasource_id required")

        url = f"/v1/datasources/{id}"
        res = await self.fetch("delete", url, None)
        return res

    async def update_datasource(self, id: str, payload: dict):
        if id is None:
            raise TypeError("datasource_id required")

        url = f"/v1/datasources/{id}"
        res = await self.fetch("put", url, payload)
        return res

    def __validate_metadata(self, metadata):
        if metadata is not None:
            if not isinstance(metadata, dict):
                raise TypeError("Metadata must be a dictionary.")
            for key, value in metadata.items():
                if not isinstance(key, str) or not (isinstance(value, str) or isinstance(value, int)):
                    raise TypeError("Metadata keys must be strings, and values must be strings or numbers.")

    async def __add_data_entity_resource(self, datasource, filename, file_size, metadata=None):
        self.__validate_metadata(metadata)
        url = '/v1/data-entities'
        payload = {
            'datasource': datasource,
            'name': self.__sanitize_filename(filename),
            'sourceType': "file",
            "metadata": metadata
        }
        headers = {'x-metal-file-size': str(file_size)}

        return await self.fetch("post", url, payload, headers=headers)

    async def add_data_entity(self, datasource, file_path, metadata=None):
        if datasource is None:
            raise ValueError("Payload must contain a 'datasource' id")

        if not os.path.exists(file_path):
            raise ValueError(f"File '{file_path}' not found.")

        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        file_type, _ = mimetypes.guess_type(file_path)

        resource = await self.__add_data_entity_resource(datasource, filename, file_size, metadata=metadata)
        if not resource or 'data' not in resource:
            logger.error("Failed to create a data entity resource.")
            return None

        await self.__upload_file_to_url(resource['data']['url'], file_path, file_type, file_size)

        return resource

    async def get_data_entity(self, id: str):
        if id is None:
            raise TypeError("data_entity_id required")

        url = f"/v1/data-entities/{id}"
        res = await self.fetch("get", url, None)
        return res

    async def delete_data_entity(self, id: str):
        if id is None:
            raise TypeError("data_entity_id required")

        url = f"/v1/data-entities/{id}"
        res = await self.fetch("delete", url, None)
        return res

    async def get_all_data_entities(self, datasource_id: str, limit=None, page=None):
        if datasource_id is None:
            raise TypeError("datasource ID required")

        url = f"/v1/datasources/{datasource_id}/data-entities"

        params = {}
        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page

        res = await self.fetch("get", url, None, params)
        return res

    async def add_index(self, payload: CreateIndexPayload) -> dict:
        url = "v1/indexes"
        res = await self.fetch("post", url, payload)
        return res

    async def get_index(self, index_id: str) -> dict:
        if not index_id:
            raise TypeError("index_id is required")

        url = f"/v1/indexes/{index_id}"
        res = await self.fetch("get", url, None)
        return res

    async def update_index(self, index_id: str, payload: UpdateIndexPayload) -> dict:
        url = f"v1/indexes/{index_id}"
        res = await self.fetch("put", url, payload)
        return res

    async def get_queries(self, index_id: str) -> dict:
        if not index_id:
            raise TypeError("index_id required")

        url = f"/v1/indexes/{index_id}/queries"

        res = await self.fetch("get", url, None)
        return res

    async def add_app(self, payload: CreateAppPayload) -> dict:
        url = "v1/apps"

        res = await self.fetch("post", url, payload)
        return res

    async def get_app(self, app_id: str) -> dict:
        if not app_id:
            raise TypeError("app_id required")
        if len(app_id) != 24:
            raise ValueError("app_id must have a length of 24 characters")

        url = f"/v1/apps/{app_id}"
        res = await self.fetch("get", url, None)
        return res

    async def get_apps(self) -> dict:
        url = "/v1/apps"

        res = await self.fetch("get", url, None)
        return res

    async def update_app(self, app_id: str, payload: UpdateAppPayload) -> dict:
        if not app_id:
            raise TypeError("app_id required")

        url = f"/v1/apps/{app_id}"
        res = await self.fetch("put", url, payload)
        return res
