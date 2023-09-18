import os
from dotenv import load_dotenv
from metal_sdk.metal import Metal

load_dotenv()

metal_api_key = os.environ["METAL_API_KEY"]
metal_client_id = os.environ["METAL_CLIENT_ID"]
metal_index_id = os.environ["METAL_INDEX_ID"]


def main():
    metal = Metal(metal_api_key, metal_client_id)

    # metal.index({ "id": "667", "text": "Dave Mustain" })
    # metal.index({ "id": "666", "text": "Ozzy" })
    # metal.index({ "id": "668", "text": "Bruce Dickenson" })
    metal.search({"text": "908", "limit": 1})


main()
