import requests

class APIClient:
    BASE_URL = "https://api.restful-api.dev/objects"

    @staticmethod
    def fetch_data():
        try:
            response = requests.get(APIClient.BASE_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []