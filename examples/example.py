import os
from dotenv import load_dotenv
from metal_sdk.metal import Metal

load_dotenv()

metal_api_key = os.environ["METAL_API_KEY"]
metal_client_id = os.environ["METAL_CLIENT_ID"]
metal_index_id = os.environ["METAL_INDEX_ID"]


def main():
    metal = Metal(metal_api_key, metal_client_id, metal_index_id)

    # metal.index({ "id": "667", "text": "Dave Mustain" })
    # metal.index({ "id": "666", "text": "Ozzy" })
    # metal.index({ "id": "668", "text": "Bruce Dickenson" })
    # result = metal.search({"text": "908", "limit": 1})
    # create datasource
    # payload = {
    #     "name": "test8",
    #     "metadataFields": [
    #     {
    #         "name": "band",
    #         "type": "String",
    #         "description": "Which heavy metal band is represented by the iconic mascot Eddie?"
    #     }
    #     ],
    #     "sourcetype": "File",
    #     "autoExtract": True
    # }
    # result = metal.create_datasource(payload)

    # get datasource
    # result = metal.get_datasource("64f7701112671601248527a9")

    # delete datasource
    # result = metal.delete_datasource("64f7701112671601248527a9")

    # update datasource
#     payload = {
        #     "name": "my_datasource",
        #     "metadataFields": [
        #       {
        #         "name": "Sales in Japan",
        #         "type": "string",
        #         "description": "How does net sales this quarter compare to the same quarter last year , three months ended?"
        #       },
        # 			      {
        #         "name": "Cost Management",
        #         "type": "string",
        #         "description": "Have operating expenses been growing disproportionately to revenues?"
        #       },
        # 						      {
        #         "name": "Cost Management",
        #         "type": "string",
        #         "description": 	"Are there any non-recurring costs that significantly impacted the 3-month or 9-month results?"
        #       },
        # 									      {
        #         "name": "Gross Margin 3 month",
        #         "type": "string",
        #         "description": 	"What is the gross margin percentage for the last 3 months?"
        #       }
        #     ],
        #     "sourcetype": "File",
        #     "autoExtract": True
        # }
#     result = metal.update_datasource("64f76ebe12671601248527a8", payload)
    # print(result)

main()
