# /backend/data_handler/mt5_client.py
import requests
from data_handler.api_client import APIClient

class MetaTrader5Client(APIClient):
    def __init__(self, mt5_url, api_key):
        super().__init__(mt5_url, api_key)

    def execute_trade(self, symbol, action, amount):
        endpoint = f"{self.base_url}/trade"
        response = requests.post(endpoint, json={
            "symbol": symbol,
            "action": action.upper(),
            "amount": amount,
            "api_key": self.api_key
        })
        return response.json()
