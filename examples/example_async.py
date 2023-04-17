import os
from dotenv import load_dotenv
from metal_sdk.metal_async import Metal

load_dotenv()

metal_api_key = os.environ["METAL_API_KEY"]
metal_client_id = os.environ["METAL_CLIENT_ID"]
metal_index_id = os.environ["METAL_INDEX_ID"]


async def main():
    metal = Metal(metal_api_key, metal_client_id, metal_index_id)

    await metal.index({"id": "667", "text": "Dave Mustain"})
    await metal.index({"id": "666", "text": "Ozzy"})
    await metal.index({"id": "668", "text": "Bruce Dickenson"})

    result = await metal.search({"text": "Black Sabbath", "limit": 1})

    print(result)
