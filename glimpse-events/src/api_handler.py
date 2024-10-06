from glimpse_api_client.glimpse_api_client import Client, models
from glimpse_api_client.glimpse_api_client.api.default import get_transcriptions

class API():

    def get_transcriptions(self):
        
        client = Client(base_url="http://localhost:8080")
        response = get_transcriptions.sync_detailed(
            client=client,
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.content}")
        return response.parsed