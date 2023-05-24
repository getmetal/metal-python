import httpx

API_URL = 'https://api.getmetal.io/v1/motorhead'

class Motorhead:
    def __init__(self, api_key=None, client_id=None, base_url=API_URL):
        self.api_key = api_key
        self.client_id = client_id
        self.base_url = base_url

        if base_url == API_URL and not (api_key and client_id):
            raise ValueError('api_key and client_id required for managed motorhead')

        self.client = httpx.Client(headers={
            'Content-Type': 'application/json',
            'x-metal-api-key': self.api_key,
            'x-metal-client-id': self.client_id,
        })

    async def add_memory(self, sessionId, payload):
        response = await self.client.post(f'{self.base_url}/sessions/{sessionId}/memory', json=payload)
        response.raise_for_status()

        data = response.json()
        memory = data.get('data', data)
        return memory

    async def get_memory(self, sessionId):
        response = await self.client.get(f'{self.base_url}/sessions/{sessionId}/memory')
        response.raise_for_status()

        data = response.json()
        memory = data.get('data', data)
        return memory

    async def delete_memory(self, sessionId):
        response = await self.client.delete(f'{self.base_url}/sessions/{sessionId}/memory')
        response.raise_for_status()

        data = response.json()
        return data.get('data', data)
