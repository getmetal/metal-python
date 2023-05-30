import httpx
from .typings import MotorheadPayload

API_URL = 'https://api.getmetal.io/v1/motorhead'


class Motorhead:
    def __init__(self, payload: MotorheadPayload = {}):
        self.api_key = payload.get("api_key")
        self.client_id = payload.get("client_id")
        self.base_url = payload.get("base_url") or API_URL

        if self.base_url == API_URL and not (self.api_key and self.client_id):
            raise ValueError('api_key and client_id required for managed motorhead')

        self.client = httpx.Client(headers={
            'Content-Type': 'application/json',
            'x-metal-api-key': self.api_key,
            'x-metal-client-id': self.client_id,
        })

    def add_memory(self, sessionId, payload):
        response = self.client.post(f'{self.base_url}/sessions/{sessionId}/memory', json=payload)
        response.raise_for_status()

        data = response.json()
        memory = data.get('data', data)
        return memory

    def get_memory(self, sessionId):
        response = self.client.get(f'{self.base_url}/sessions/{sessionId}/memory')
        response.raise_for_status()

        data = response.json()
        memory = data.get('data', data)
        return memory

    def delete_memory(self, sessionId):
        response = self.client.delete(f'{self.base_url}/sessions/{sessionId}/memory')
        response.raise_for_status()

        data = response.json()
        return data.get('data', data)
