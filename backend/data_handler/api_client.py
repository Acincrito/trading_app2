# /backend/data_handler/api_client.py

import requests

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key

    def get_headers(self):
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def send_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self.get_headers()
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError("Método HTTP não suportado")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
