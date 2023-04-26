import httpx
from .typings import IndexPayload, SearchPayload, TunePayload


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

    def __validateIndexAndSearch(self, index=None, payload={}):
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
        self.__validateIndexAndSearch(index, payload)
        data = self.__getData(index, payload)
        url = "/v1/index"

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()

    def search(
        self, payload: SearchPayload = {}, index_id=None, ids_only=False, limit=1
    ):
        index = index_id or self.index_id
        self.__validateIndexAndSearch(index, payload)
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
        if id is None:
            raise TypeError("id required")

        url = "/v1/documents/" + id

        res = self.request("get", url)
        res.raise_for_status()
        return res.json()

    def delete_one(self, id: str, index_id=None):
        if id is None:
            raise TypeError("id required")

        url = "/v1/documents/" + id

        res = self.request("delete", url)
        res.raise_for_status()
        return res.json()
