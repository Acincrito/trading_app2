from websocket import WebSocketApp

class WebsocketClient:
    def __init__(self):
        self.ws = WebSocketApp("wss://your.websocket.url",
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)

    def on_message(self, ws, message):
        print("Received message:", message)

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def run(self):
        self.ws.run_forever()

if __name__ == "__main__":
    client = WebsocketClient()
    client.run()

