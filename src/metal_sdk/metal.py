import os
import mimetypes
import httpx
from typing import List
from .typings import IndexPayload, SearchPayload, TunePayload, BulkIndexItem


BASE_API = "https://api.getmetal.io"


class Metal(httpx.Client):
    api_key: str
    client_id: str
    index_id: str

    def __init__(self, api_key, client_id, index_id=None, base_url=BASE_API):
        super().__init__()
        self.api_key = api_key
        self.client_id = client_id
        self.index_id = index_id
        self.headers.update({
            'Content-Type': 'application/json',
            'x-metal-api-key': self.api_key,
            'x-metal-client-id': self.client_id,
        })
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        return super().request(method, url, *args, **kwargs)

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

    def index(self, payload: IndexPayload = {}, index_id=None):
        index = self.index_id or index_id
        self.__validateIndex(index, payload)
        data = self.__getData(index, payload)
        url = "/v1/index"

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()

    def index_many(self, payload: List[BulkIndexItem]):
        url = "/v1/index/bulk"
        data = {"data": payload}

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()

    def search(
        self, payload: SearchPayload = {}, index_id=None, ids_only=False, limit=1
    ):
        index = index_id or self.index_id

        if index is None:
            raise TypeError("index_id required")

        data = self.__getData(index, payload)

        url = "/v1/search?limit=" + str(limit)

        if ids_only:
            url = url + "&idsOnly=true"

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()

    def tune(self, payload: TunePayload = {}, index_id=None):
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

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()

    def get_one(self, id: str, index_id=None):
        index = index_id or self.index_id

        if id is None:
            raise TypeError("id required")

        if index is None:
            raise TypeError("index_id required")

        url = "/v1/indexes/" + index + "/documents/" + id

        res = self.request("get", url)
        res.raise_for_status()
        return res.json()

    def delete_one(self, id: str, index_id=None):
        index = index_id or self.index_id

        if id is None:
            raise TypeError("id required")

        if index is None:
            raise TypeError("index_id required")

        url = "/v1/indexes/" + index + "/documents/" + id

        res = self.request("delete", url)
        res.raise_for_status()

        return None

    def delete_many(self, ids: List[str], index_id=None):
        index = index_id or self.index_id

        if index is None:
            raise TypeError("index_id required")

        if ids is None:
            raise TypeError("ids required")

        url = f'/v1/indexes/{index}/documents/bulk'

        res = self.request("delete", url, json={"ids": ids})
        res.raise_for_status()

        return None

    def __sanitize_filename(self, filename):
        """
        Implement your filename sanitation method here.
        """
        sanitized_filename = filename.replace(' ', '_')  # Simplified example
        return sanitized_filename

    def __create_resource(self, index_id, filename, file_type, file_size):
        url = f'{self.base_url}/v1/indexes/{index_id}/files'
        payload = {
            'fileName': self.__sanitize_filename(filename),
            'fileType': file_type,
        }
        headers = {'x-metal-file-size': str(file_size)}

        res = self.request("post", url, json=payload, headers=headers)
        res.raise_for_status()  # Raise exception if the request failed

        return res.json()

    def __upload_file_to_url(self, url, file_path, file_type, file_size):
        with open(file_path, 'rb') as f:
            headers = {
                'content-type': file_type,
                'content-length': str(file_size),
            }
            res = self.request("put", url, data=f, headers=headers)

        res.raise_for_status()  # Raise exception if the request failed
        return res

    def upload_file(self, file_path, index_id=None):
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
        resource = self.__create_resource(index, filename, file_type, file_size)

        # Upload the file to the returned url
        self.__upload_file_to_url(resource['data']['url'], file_path, file_type, file_size)
