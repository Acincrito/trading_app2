# /backend/api_clients/binance_bot.py

from binance.client import Client

class BinanceBot:
    def __init__(self, api_key, api_secret):
        """Inicializa o bot Binance com as credenciais fornecidas."""
        self.client = Client(api_key, api_secret)

    def place_order(self, symbol, side, quantity, price):
        """Executa uma ordem de compra ou venda na Binance com os parâmetros fornecidos."""
        order = self.client.order_limit(
            symbol=symbol,
            side=side,  # 'BUY' ou 'SELL'
            quantity=quantity,
            price=price
        )
        return order

    def get_balance(self):
        """Obtém o saldo da conta (exemplo com USDT)."""
        balance = self.client.get_asset_balance(asset='USDT')  # Substitua 'USDT' se necessário
        return balance
