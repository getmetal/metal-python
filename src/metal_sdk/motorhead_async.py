import httpx
from .typings import MotorheadPayload

API_URL = 'https://api.getmetal.io/v1/motorhead/'


class Motorhead(httpx.AsyncClient):
    def __init__(self, payload: MotorheadPayload = {}):
        super().__init__()
        self.api_key = payload.get("api_key")
        self.client_id = payload.get("client_id")
        self.base_url = payload.get("base_url") or API_URL

        has_api_key = self.api_key is not None
        has_client_id = self.client_id is not None
        has_key_and_id = has_api_key and has_client_id

        if self.base_url == API_URL and not has_key_and_id:
            raise ValueError('api_key and client_id required for managed motorhead')

        self.headers.update({
            'Content-Type': 'application/json',
            'x-metal-api-key': self.api_key,
            'x-metal-client-id': self.client_id,
        })

    async def request(self, method, url, *args, **kwargs):
        return await super().request(method, url, *args, **kwargs)

    async def add_memory(self, sessionId, payload):
        url = f'/sessions/{sessionId}/memory'
        res = await self.request("post", url, json=payload)
        res.raise_for_status()

        data = res.json()
        memory = data.get('data', data)
        return memory

    async def get_memory(self, sessionId):
        url = f'/sessions/{sessionId}/memory'
        res = await self.request("get", url)
        res.raise_for_status()
        data = res.json()
        memory = data.get('data', data)
        return memory

    async def delete_memory(self, sessionId):
        url = f'/sessions/{sessionId}/memory'
        res = await self.request("delete", url)
        res.raise_for_status()

        return
