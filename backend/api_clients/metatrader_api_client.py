# /backend/api_clients/metatrader_api_client.py

import MetaTrader5 as mt5
import requests
from typing import Dict, Any


class MetaTraderBase:
    """Classe base comum para interagir com o MetaTrader, seja via MetaTrader 5 (MT5) ou via API HTTP."""

    def __init__(self, login=None, password=None, server=None, base_url=None):
        """Inicializa o cliente com as credenciais de login ou URL base da API, dependendo da implementação."""
        self.login = login
        self.password = password
        self.server = server
        self.base_url = base_url

    def login(self) -> Dict[str, Any]:
        """Método de login genérico, a ser implementado nas subclasses."""
        raise NotImplementedError

    def execute_trade(self, symbol: str, action: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Método de execução de trade genérico, a ser implementado nas subclasses."""
        raise NotImplementedError

    def get_balance(self) -> float:
        """Método de verificação de saldo genérico, a ser implementado nas subclasses."""
        raise NotImplementedError


class MetaTraderBot(MetaTraderBase):
    """Implementação do MetaTraderBot utilizando a biblioteca MetaTrader5 (MT5)."""

    def __init__(self, login: str, password: str, server: str):
        """Inicializa o bot com as credenciais do MetaTrader 5."""
        super().__init__(login, password, server)
        if not mt5.initialize():
            raise Exception("Falha ao conectar ao MetaTrader 5")

    def login(self) -> Dict[str, Any]:
        """Realiza o login no MetaTrader 5 e retorna o status da conexão."""
        # Não há autenticação explícita no MetaTrader 5, pois já se conecta no momento de inicialização.
        return {"status": "success", "message": "Conectado ao MetaTrader 5"}

    def execute_trade(self, symbol: str, action: str, amount: float, price: float, order_type: int, stop_loss: float, take_profit: float) -> Dict[str, Any]:
        """Envia uma ordem de compra ou venda no MetaTrader 5."""
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": amount,
            "price": price,
            "type": order_type,  # Tipo de ordem (compra/venda)
            "sl": stop_loss,     # Stop Loss
            "tp": take_profit,   # Take Profit
            "deviation": 20,     # Desvio máximo permitido para execução
            "magic": 234000,     # Identificador único da ordem
            "comment": "Test order",  # Comentário opcional
            "type_filling": mt5.ORDER_FILLING_IOC,  # Tipo de preenchimento
            "type_time": mt5.ORDER_TIME_GTC  # Tipo de tempo (GTC = Good 'Til Canceled)
        }
        result = mt5.order_send(order)  # Envia a ordem
        return result

    def get_balance(self) -> float:
        """Obtém o saldo da conta MetaTrader 5."""
        account_info = mt5.account_info()  # Obtém informações da conta
        if account_info is None:
            return {"status": "error", "message": "Falha ao obter informações da conta"}
        balance = account_info.balance  # Retorna o saldo
        return balance


class MetaTraderAPIClient(MetaTraderBase):
    """Implementação do MetaTrader utilizando a API HTTP."""

    def __init__(self, base_url: str):
        """Inicializa o cliente com a URL base da API."""
        super().__init__(base_url=base_url)

    def login(self) -> Dict[str, Any]:
        """Simula o login na API MetaTrader e retorna a resposta fictícia."""
        # A autenticação na API pode ser personalizada
        return {"status": "success", "message": "Conectado ao servidor MetaTrader via API"}

    def execute_trade(self, symbol: str, action: str, amount: float, **kwargs) -> Dict[str, Any]:
        """Executa uma operação de trade (compra/venda) via API HTTP."""
        endpoint = f"{self.base_url}/trade"
        data = {
            "symbol": symbol,
            "action": action,  # 'buy' ou 'sell'
            "amount": amount,
            "order_type": "market"  # Tipo de ordem: mercado
        }
        try:
            response = requests.post(endpoint, json=data)
            response.raise_for_status()  # Lança erro em caso de falha na requisição
            return response.json()
        except requests.exceptions.RequestException as e:
            # Retorna erro caso a requisição falhe
            return {"status": "error", "message": str(e)}

    def get_balance(self) -> float:
        """Obtém o saldo da conta via API HTTP."""
        try:
            response = requests.get(f"{self.base_url}/balance", params={"username": self.login})
            response.raise_for_status()
            return response.json().get("balance", 0)
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
