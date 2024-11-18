# /backend/data_handler/binance_client.py
import hashlib
import hmac
import time
import requests
from data_handler.api_client import APIClient

class BinanceClient(APIClient):
    def __init__(self, base_url, api_key, secret_key):
        super().__init__(base_url, api_key)
        self.secret_key = secret_key

    def _sign_request(self, data):
        query_string = '&'.join([f"{k}={v}" for k, v in data.items()])
        signature = hmac.new(self.secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        return f"{query_string}&signature={signature}"

    def execute_trade(self, symbol, action, amount):
        endpoint = f"{self.base_url}/api/v3/order"
        data = {
            "symbol": symbol,
            "side": action.upper(),
            "type": "MARKET",
            "quantity": amount,
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000
        }
        signed_data = self._sign_request(data)
        headers = {"X-MBX-APIKEY": self.api_key}
        response = requests.post(endpoint, params=signed_data, headers=headers)
        return response.json()
