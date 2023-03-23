import requests
from urllib.parse import urljoin
from .typings import IndexPayload, SearchPayload, TunePayload


BASE_API = "https://api.getmetal.io/v1"


class Metal(requests.Session):
    api_key: str
    client_id: str
    app_id: str

    def __init__(self, api_key, client_id, app_id=None, base_url=BASE_API):
        super().__init__()
        self.api_key = api_key
        self.client_id = client_id
        self.app_id = app_id
        self.headers.update({
            'Content-Type': 'application/json',
            'x-metal-api-key': self.api_key,
            'x-metal-client-id': self.client_id,
        })
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        return super().request(method, urljoin(self.base_url, url), *args, **kwargs)

    def __get_headers(self):
        return {
            "Content-Type": "application/json",
            "x-metal-api-key": self.api_key,
            "x-metal-client-id": self.client_id,
        }

    def __getData(self, app, payload: dict = {}):
        data = {"app": app}
        if payload.get("id") is not None:
            data["id"] = payload["id"]

        if payload.get("imageBase64") is not None:
            data["imageBase64"] = payload["imageBase64"]
        elif payload.get("imageUrl") is not None:
            data["imageUrl"] = payload["imageUrl"]
        elif payload.get("text") is not None:
            data["text"] = payload["text"]
        elif payload.get("embedding") is not None:
            data["embedding"] = payload["embedding"]

        return data

    def __validateIndexAndSearch(self, app=None, payload={}):
        if app is None:
            raise TypeError("app_id required")

        if (
            payload.get("imageBase64") is None
            and payload.get("imageUrl") is None
            and payload.get("text") is None
            and payload.get("embedding") is None
        ):
            raise TypeError("imageBase64, imageUrl, text, or embedding required")

    def index(self, payload: IndexPayload = {}, app_id=None):
        app = self.app_id or app_id
        self.__validateIndexAndSearch(app, payload)
        data = self.__getData(app, payload)
        url = "/index"

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()

    def search(
        self, payload: SearchPayload = {}, app_id=None, ids_only=False
    ):
        app = app_id or self.app_id
        self.__validateIndexAndSearch(app, payload)
        data = self.__getData(app, payload)

        url = "/search"

        if ids_only:
            url = url + "?idsOnly=true"

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()

    def tune(self, payload: TunePayload = {}, app_id=None):
        app = app_id or self.app_id

        if app is None:
            raise TypeError("app_id required")

        idA = payload.get("idA")
        idB = payload.get("idB")
        label = payload.get("label")

        if idA is None or idB is None or label is None:
            raise TypeError("idA, idB, and label required")

        url = "/tune"
        data = {"app": app, "idA": idA, "idB": idB, "label": label}

        res = self.request("post", url, json=data)
        res.raise_for_status()
        return res.json()
