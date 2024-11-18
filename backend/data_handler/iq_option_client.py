# /backend/data_handler/iq_option_client.py
import websocket
import json
from data_handler.api_client import APIClient

class IQOptionClient(APIClient):
    def __init__(self, iq_option_url, api_key):
        super().__init__(iq_option_url, api_key)
        self.ws = websocket.WebSocket()

    def connect(self):
        self.ws.connect(self.base_url)
        login_data = json.dumps({"name": "ssid", "msg": self.api_key})
        self.ws.send(login_data)

    def execute_trade(self, symbol, action, amount):
        self.connect()
        trade_data = json.dumps({
            "name": "buyV2",
            "msg": {
                "instrument_id": symbol,
                "direction": action.lower(),
                "amount": amount
            }
        })
        self.ws.send(trade_data)
        response = self.ws.recv()
        self.ws.close()
        return json.loads(response)
