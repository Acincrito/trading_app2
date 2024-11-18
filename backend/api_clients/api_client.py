# /backend/api_clients/api_client.py

import requests
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
from functools import lru_cache

# Configuração do logger
logger = logging.getLogger("APIClient")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class APIClient(ABC):
    """
    Classe base para clientes de APIs. Lida com a autenticação e envio de requisições HTTP.
    Subclasses devem implementar o método `execute_trade` para operações específicas.
    """

    def __init__(self, base_url: str, api_key: str = None):
        """
        Inicializa o cliente da API com a URL base e a chave da API (se necessário).
        
        :param base_url: URL base da API.
        :param api_key: Chave da API (opcional).
        """
        self.base_url = base_url
        self.api_key = api_key

    def get_headers(self) -> Dict[str, str]:
        """
        Retorna os cabeçalhos da requisição, incluindo o token de autenticação, se fornecido.

        :return: Cabeçalhos para a requisição HTTP.
        """
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def send_request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> Dict[str, Any]:
        """
        Envia uma requisição HTTP para a API especificada.
        
        :param method: Método HTTP (GET ou POST).
        :param endpoint: Endpoint da API.
        :param data: Dados para enviar no corpo da requisição (para POST).
        :param params: Parâmetros para enviar na URL (para GET).
        :return: Resposta da API em formato JSON.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = self.get_headers()

        try:
            logger.info(f"Enviando requisição {method} para {url} com dados: {data} e parâmetros: {params}")
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError("Método HTTP não suportado")
            response.raise_for_status()
            logger.info(f"Resposta recebida: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição: {str(e)}")
            return {"status": "error", "message": str(e)}

    def validate_trade_parameters(self, symbol: str, action: str, amount: float):
        """
        Valida os parâmetros passados para a operação de trade.

        :param symbol: Símbolo do ativo (ex: 'EURUSD').
        :param action: Ação do trade ('buy' ou 'sell').
        :param amount: Quantidade do ativo a ser negociado.
        :raises ValueError: Se algum parâmetro for inválido.
        """
        if not isinstance(symbol, str) or len(symbol) == 0:
            raise ValueError("O símbolo deve ser uma string não vazia.")
        if action not in ["buy", "sell"]:
            raise ValueError("Ação inválida. Use 'buy' ou 'sell'.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("A quantidade deve ser um número positivo.")

    @abstractmethod
    def execute_trade(self, symbol: str, action: str, amount: float) -> Dict[str, Any]:
        """
        Método abstrato para execução de trades. Deve ser implementado nas subclasses.

        :param symbol: Símbolo do ativo.
        :param action: Ação do trade ('buy' ou 'sell').
        :param amount: Quantidade a ser negociada.
        :return: Resultado da execução do trade.
        """
        pass

    @lru_cache(maxsize=128)
    def get_cached_balance(self) -> float:
        """
        Exemplo de função onde o cache pode ser útil. Aqui, simula uma chamada para obter o saldo.
        O LRU cache armazena até 128 resultados dessa função para evitar múltiplas consultas.

        :return: Saldo simulado.
        """
        logger.info("Obtendo saldo...")
        # Simula uma chamada para obter saldo da API
        return 1000.0  # Exemplo de saldo retornado pela API


class MetaTraderAPIClient(APIClient):
    """
    Cliente para interagir com a API do MetaTrader.
    """

    def __init__(self, base_url: str, login: str, password: str, server: str, api_key: str = None):
        """
        Inicializa o cliente MetaTrader com credenciais.

        :param base_url: URL base da API do MetaTrader.
        :param login: Login da conta MetaTrader.
        :param password: Senha da conta MetaTrader.
        :param server: Servidor MetaTrader.
        :param api_key: Chave da API (opcional).
        """
        super().__init__(base_url, api_key)
        self.login = login
        self.password = password
        self.server = server

    def execute_trade(self, symbol: str, action: str, amount: float) -> Dict[str, Any]:
        """
        Executa uma operação de compra ou venda no MetaTrader.

        :param symbol: Símbolo do ativo.
        :param action: Ação ('buy' ou 'sell').
        :param amount: Quantidade a ser negociada.
        :return: Resultado da execução do trade.
        """
        self.validate_trade_parameters(symbol, action, amount)
        data = {
            "symbol": symbol,
            "action": action,
            "amount": amount,
            "order_type": "market"
        }
        endpoint = "trade"
        return self.send_request("POST", endpoint, data=data)


class IQOptionAPIClient(APIClient):
    """
    Cliente para interagir com a API da IQ Option.
    """

    def __init__(self, username: str, password: str, base_url: str, api_key: str = None):
        """
        Inicializa o cliente IQ Option com credenciais.

        :param username: Nome de usuário da IQ Option.
        :param password: Senha da IQ Option.
        :param base_url: URL base da API da IQ Option.
        :param api_key: Chave da API (opcional).
        """
        super().__init__(base_url, api_key)
        self.username = username
        self.password = password

    def execute_trade(self, symbol: str, action: str, amount: float) -> Dict[str, Any]:
        """
        Executa uma operação de compra ou venda na IQ Option.

        :param symbol: Símbolo do ativo.
        :param action: Ação ('buy' ou 'sell').
        :param amount: Quantidade a ser negociada.
        :return: Resultado da execução do trade.
        """
        self.validate_trade_parameters(symbol, action, amount)
        data = {
            "symbol": symbol,
            "action": action,
            "amount": amount,
        }
        endpoint = "trade"
        return self.send_request("POST", endpoint, data=data)


# Exemplos de uso

meta_trader = MetaTraderAPIClient(base_url="https://api.metatrader.com", login="user", password="password", server="server")
response = meta_trader.execute_trade("EURUSD", "buy", 1.0)
print(response)

iq_option = IQOptionAPIClient(username="user", password="password", base_url="https://api.iqoption.com")
response = iq_option.execute_trade("EURUSD", "sell", 10.0)
print(response)

# Exemplo de uso do cache de saldo
meta_trader_balance = meta_trader.get_cached_balance()
print(f"Saldo do MetaTrader: {meta_trader_balance}")
